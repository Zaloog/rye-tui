from typing import Iterable
from pathlib import Path
import tomllib

from rich.table import Table
from textual import on, work
from textual.events import Resize
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, ListView, RichLog
from rich_pixels import Pixels

from rye_tui.components.helper_widgets import ProjectListItem
from rye_tui.components.modals import (
    ModalRyeInit,
    ModalRyePin,
    ModalRyeAdd,
    ModalConfirm,
)
from rye_tui.utils import rye_command_str_output, delete_folder
from rye_tui.constants import IMAGE_PATH


class ProjectTab(Container):
    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            with Vertical():
                yield ProjectList()
                yield ProjectInteraction()
            with Vertical():
                yield ProjectPreview()

        return super().compose()


class ProjectList(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Project List"
        self.id = "project_list"

        yield ListView(
            *[
                ProjectListItem(project_title=proj)
                for proj in self.app.cfg.project_names
            ],
            initial_index=None,
        )

        return super().compose()

    async def update(self):
        self.remove()
        self.app.mount(ProjectList(), before="#project_interaction")

    @on(ListView.Selected)
    def get_project_infos(self, event: ListView.Selected):
        self.app.get_project_infos(project_name=event.item.project_title)

        self.log.error(self.app.project)

        self.app.active_project = event.item.project_title
        self.app.active_project_path = self.app.cfg.config["projects"].get(
            self.app.active_project
        )
        with open(
            Path(self.app.active_project_path) / "pyproject.toml", "rb"
        ) as tomlfile:
            self.app.active_project_toml = tomllib.load(tomlfile)

        try:
            with open(
                Path(self.app.active_project_path) / "requirements.lock", "r"
            ) as lockfile:
                self.app.active_project_lock = [
                    line.split("==")[0]
                    for line in lockfile.readlines()
                    if not line.startswith("#")
                ]
        except FileNotFoundError:
            self.notify(
                title="File not found",
                message=f"[blue]requirements.lock[/] is not present yet for [blue]{self.app.active_project}[/]",
                severity="error",
            )

        preview_window = self.app.query_one("#project_preview")
        preview_window.update_content()
        preview_window.border_subtitle = self.app.active_project

        btns = self.app.query("ProjectListItem Button")
        for btn in btns:
            btn.add_class("invisible")

        event.item.query(Button).remove_class("invisible")

    @on(Button.Pressed, ".delete-button")
    def delete_project(self, message):
        self.log.error(message)

        def check_delete(delete_files: bool) -> None:
            if delete_files:
                self.app.log.error("deleted all")
                res = delete_folder(folder_path=self.app.active_project_path)
                self.log.error(res)

            else:
                self.app.log.error("deleted not all")

            project_list = self.app.query_one(ListView)

            for i, project in enumerate(project_list.children):
                if project.id == self.app.active_project:
                    project_list.pop(i)

            self.app.cfg.remove_project(self.app.active_project)
            self.app.reset_project()

        self.app.push_screen(ModalConfirm(), check_delete)


class ProjectInteraction(Container):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Interaction"
        self.id = "project_interaction"

        with Vertical():
            with Horizontal():
                yield Button("New Project", id="btn_new")
                yield Button("Add/Remove Packages", id="btn_pkg")
                yield Button("Rye Sync + Update", id="btn_sync")
            with Horizontal():
                yield Button("Pin Python Version", id="btn_pin")
                yield Button("Build", id="btn_build")
                yield Button("Publish", id="btn_publish")

        return super().compose()

    @on(Button.Pressed, "#btn_publish")
    async def rye_load_package_list(self) -> None:
        # Open new Modal
        self.app.cfg.add_project(
            new_project_name="test2", new_project_path=Path().cwd().as_posix()
        )

        # Testing
        project_list = self.app.query_one(ListView)
        project_list.append(item=ProjectListItem(project_title="test2"))
        num_project = project_list.children.__len__()
        project_list.index = num_project
        project_list.action_select_cursor()

    @on(Button.Pressed, "#btn_new")
    def rye_init_new_project(self) -> None:
        self.app.push_screen(ModalRyeInit())

    @on(Button.Pressed, "#btn_pkg")
    def rye_add_packages(self) -> None:
        self.app.push_screen(ModalRyeAdd())

    @on(Button.Pressed, "#btn_pin")
    def rye_pin_python_version(self) -> None:
        self.app.push_screen(ModalRyePin())

    @work(thread=True)
    @on(Button.Pressed, "#btn_sync")
    async def rye_sync_project(self) -> None:
        self.app.query_one("#project_preview").loading = True
        await self.async_sync_function()
        self.app.query_one("#project_preview").loading = False

    async def async_sync_function(self):
        output = rye_command_str_output(
            command="rye sync -f", cwd=self.app.active_project_path
        )
        self.app.query_one(ListView).action_select_cursor()
        return output


class ProjectPreview(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Preview"
        self.border_subtitle = "no project selected"
        self.id = "project_preview"
        self.content_info = RichLog(wrap=False, auto_scroll=True)

        yield self.content_info

        return super().compose()

    @work(thread=True, exclusive=True)
    def update_content(self):
        try:
            if self.app.project["path"]:
                project_infos = rye_command_str_output(
                    "rye show", cwd=self.app.active_project_path
                )
                project_packages = rye_command_str_output(
                    "rye list", cwd=self.app.active_project_path
                )
                self.content_info.clear()
                self.content_info.write(project_infos)
                self.content_info.write(self.app.project["toml"])

                table = Table("package", "version", expand=True)
                for pkg in project_packages.split("\n"):
                    if "==" in pkg:
                        pkg_name, pkg_version = pkg.split("==")
                        table.add_row(pkg_name, pkg_version)

                self.content_info.write(table)

            else:
                content = "please select a project"
                self.content_info.clear()
                self.content_info.write(content)
            # self.content = content
        except Exception:
            self.content_info.clear()
            self.content_info.write("error: project path name is not valid")

    @on(Resize)
    def keep_image_size(self, event: Resize):
        if not self.app.project["name"]:
            new_width, new_height = event.size
            pixels = Pixels.from_image_path(
                IMAGE_PATH,
                resize=(new_width, int(1.8 * new_height)),
            )
            self.content_info.clear()
            self.content_info.write(pixels)
