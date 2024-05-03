from typing import Iterable
from pathlib import Path

from rich.table import Table
from textual import on, work
from textual.events import Resize
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, ListView, RichLog
from rich_pixels import Pixels

from rye_tui.components.helper_widgets import ProjectListItem
from rye_tui.components.modals import ModalRyeInit, ModalRyePin
from rye_tui.rye_commands import rye_command_str_output
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
        # self.app.query_one(ProjectList).focus()

    @on(ListView.Selected)
    def get_project_infos(self, event: ListView.Selected):
        self.app.active_project = event.item.project_title
        self.app.active_project_path = self.app.cfg.config["projects"].get(
            self.app.active_project
        )

        self.app.query_one("#project_preview").update_content()


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

        await self.app.query_one("#project_list").update()
        self.app.log.debug([(p, j) for p, j in self.app.cfg.config["projects"].items()])

    @on(Button.Pressed, "#btn_new")
    def rye_init_new_project(self) -> None:
        self.app.push_screen(ModalRyeInit())

    @on(Button.Pressed, "#btn_pin")
    def rye_pin_python_version(self) -> None:
        self.app.push_screen(ModalRyePin())

    @work(thread=True)
    @on(Button.Pressed, "#btn_sync")
    async def rye_sync_project(self) -> None:
        self.app.query_one("#project_preview").loading = True
        output = await self.aync_sync_function()
        self.app.log.error(output)
        self.app.query_one("#project_list").update()
        self.app.query_one("#project_preview").loading = False

    async def aync_sync_function(self):
        output = rye_command_str_output(
            command="rye sync -f", cwd=self.app.active_project_path
        )
        return output


class ProjectPreview(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Preview"
        self.id = "project_preview"
        self.content_info = RichLog(wrap=False, auto_scroll=True)

        yield self.content_info

        return super().compose()

    @work(thread=True, exclusive=True)
    def update_content(self):
        try:
            if self.app.active_project_path:
                project_infos = rye_command_str_output(
                    "rye show", cwd=self.app.active_project_path
                )
                project_packages = rye_command_str_output(
                    "rye list", cwd=self.app.active_project_path
                )
                self.content_info.clear()
                self.content_info.write(project_infos)

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
        except Exception as e:
            self.app.log.error(e)
            self.content_info.clear()
            self.content_info.write("error: project path name is not valid")

    @on(Resize)
    def keep_image_size(self, event: Resize):
        if not self.app.active_project:
            new_width, new_height = event.size
            pixels = Pixels.from_image_path(
                IMAGE_PATH,
                resize=(new_width, int(1.8 * new_height)),
            )
            self.content_info.clear()
            self.content_info.write(pixels)
