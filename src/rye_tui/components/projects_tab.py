from typing import Iterable
from pathlib import Path

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
from rye_tui.utils import (
    rye_command_str_output,
    delete_folder,
    display_toml_project_infos,
    display_general_project_infos,
)
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


########################################################################################
# Project List
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
        )

        return super().compose()

    def on_mount(self):
        self.query_one(ListView).index = None

    @on(ListView.Selected)
    def get_project_infos(self, event: ListView.Selected):
        self.app.get_project_infos(project_name=event.item.project_title)

        preview_window = self.app.query_one("#project_preview")
        preview_window.update_content()

        btns = self.app.query("ProjectListItem Button")
        for btn in btns:
            btn.add_class("invisible")

        event.item.query(Button).remove_class("invisible")

    @on(Button.Pressed, ".delete-button")
    def delete_project(self, message):
        def check_delete(delete_files: bool) -> None:
            if delete_files:
                delete_folder(folder_path=self.app.project["path"])

            project_list = self.app.query_one(ListView)

            for i, project in enumerate(project_list.children):
                if project.id == self.app.project["name"]:
                    project_list.pop(i)

            self.app.cfg.remove_project(self.app.project["name"])
            self.app.reset_project()

        self.app.push_screen(ModalConfirm(), check_delete)


########################################################################################
# Project Interaction
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
            command="rye sync -f", cwd=self.app.project["path"]
        )
        self.app.query_one(ListView).action_select_cursor()
        return output


########################################################################################
# Project Preview
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
        self.loading = True
        try:
            if self.app.project["path"]:
                self.content_info.clear()

                # path
                # python version
                # sources
                general_table = display_general_project_infos(
                    path=self.app.project["path"]
                )
                self.content_info.write(general_table, expand=True)

                # project_packages = rye_command_str_output(
                #     "rye list", cwd=self.app.project["path"]
                # )
                toml_table = display_toml_project_infos(
                    toml=self.app.project["toml"], header=True
                )
                self.content_info.write(toml_table, expand=True)

                # table = Table("package", "version", expand=True)
                # for pkg in project_packages.split("\n"):
                #     if "==" in pkg:
                #         pkg_name, pkg_version = pkg.split("==")
                #         table.add_row(pkg_name, pkg_version)

                # self.content_info.write(table)

                self.border_subtitle = self.app.project["name"]

            else:
                content = "please select a project"
                self.content_info.clear()
                self.content_info.write(content)
            # self.content = content
        except Exception:
            self.content_info.clear()
            self.content_info.write("error: project path name is not valid")

        self.loading = False

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
