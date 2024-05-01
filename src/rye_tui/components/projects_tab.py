from typing import Iterable
from pathlib import Path

from textual import on
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Static, ListView

from rye_tui.components.helper_widgets import ProjectListItem


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
                for proj, _proj_path in self.app.cfg.projects.items()
            ]
        )

        return super().compose()

    def update(self):
        self.remove()
        self.app.mount(ProjectList(), before="#project_interaction")


class ProjectInteraction(Container):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Interaction"
        self.id = "project_interaction"

        with Vertical():
            with Horizontal():
                yield Button("New Project", id="btn_new")
                yield Button("Add/Remove Packages", id="btn_pkg")
                yield Button("Rye Synch + Update")
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

        content = open(r"pyproject.toml").read()
        project_infos = Static("[green]Hello[/]\n" + content, expand=True)

        yield project_infos

        return super().compose()
