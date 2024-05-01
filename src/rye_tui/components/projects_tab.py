from typing import Iterable
from pathlib import Path

from textual import on, work
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Static, ListView

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
                for proj, _proj_path in self.app.cfg.projects.items()
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
        self.content = Static("please select a project", expand=True)

        yield self.content

        return super().compose()

    @work(thread=True)
    def update_content(self):
        try:
            if self.app.active_project_path:
                content = rye_command_str_output(
                    "rye show", cwd=self.app.active_project_path
                )
            else:
                content = "please select a project"
            self.content.update(content)
        except Exception as e:
            self.app.log.error(e)
            self.content.update("error: project path name is not valid")
