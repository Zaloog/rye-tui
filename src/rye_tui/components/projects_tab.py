from typing import Iterable
from pathlib import Path

from textual import on, work
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Static, ListView, DataTable
from rich_pixels import Pixels

from rye_tui.components.helper_widgets import ProjectListItem
from rye_tui.rye_commands import rye_command_str_output


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

    def update(self):
        self.remove()
        self.app.mount(ProjectList(), before="#project_interaction")

    @on(ListView.Selected)
    def get_project_infos(self, event: ListView.Selected):
        self.app.active_project = event.item.project_title
        self.app.active_project_path = self.app.cfg.config["projects"].get(
            self.app.active_project
        )

        self.app.query_one("#project_preview").update_content()
        self.app.log.error(self.app.active_project_path)


class ProjectInteraction(Container):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Interaction"
        self.id = "project_interaction"

        with Vertical():
            with Horizontal():
                yield Button("New Project", id="btn_new")
                yield Button("Add/Remove Packages", id="btn_pkg")
                yield Button("Rye Sync + Update")
            with Horizontal():
                yield Button("Pin Python Version")
                yield Button("Build")
                yield Button("Publish", id="btn_publish")

        return super().compose()

    @on(Button.Pressed, "#btn_publish")
    def rye_load_package_list(self) -> None:
        self.app.log.debug([(p, j) for p, j in self.app.cfg.config["projects"].items()])

    @on(Button.Pressed, "#btn_new")
    def rye_init_new_project(self) -> None:
        # Open new Modal
        self.app.cfg.add_project(
            new_project_name="test2", new_project_path=Path().cwd().as_posix()
        )
        self.app.log.error([(p, j) for p, j in self.app.cfg.config["projects"].items()])

        self.app.query_one(ProjectList).update()


# TODO
# Collapsibles Infos/Packages
## Rye show
## Rye list
class ProjectPreview(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Preview"
        self.id = "project_preview"
        # with Image.open('images/rye_image.jpg') as image:
        pixels = Pixels.from_image_path("images/rye_image.jpg", resize=(80, 55))
        self.content_info = Static(pixels, shrink=True, expand=True)
        self.content_table = DataTable(show_cursor=False, show_header=False)
        self.content_table.add_columns("package", "version")
        # self.content = Static("please select a project", expand=True)

        yield self.content_info
        yield self.content_table

        return super().compose()

    @work(thread=True)
    def update_content(self):
        try:
            if self.app.active_project_path:
                project_infos = rye_command_str_output(
                    "rye show", cwd=self.app.active_project_path
                )
                project_packages = rye_command_str_output(
                    "rye list", cwd=self.app.active_project_path
                )
                content = project_infos
                self.content_info.update(content)

                self.content_table.show_header = True
                if not self.content_table.columns:
                    self.content_table.add_columns("package", "version")
                self.content_table.clear()
                self.content_table.add_rows(
                    [i.split("==") for i in project_packages.split("\n") if "==" in i]
                )
            else:
                content = "please select a project"
                self.content_info.update(content)
                self.content_table.clear(columns=True)
            # self.content = content
        except Exception as e:
            self.app.log.error(e)
            self.content_info.update("error: project path name is not valid")
