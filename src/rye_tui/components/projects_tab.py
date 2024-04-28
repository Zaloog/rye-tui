from typing import Iterable
from pathlib import Path
import subprocess

from textual import work, on
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label, Button, Static, ListView, ListItem


class ProjectTab(Container):
    info = Static("TestStatic")

    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            with Vertical():
                yield ProjectList()
                yield ProjectInteraction()
            with Vertical():
                yield ProjectPreview()

        return super().compose()

    @on(Button.Pressed)
    def rye_load_package_list(self) -> None:
        self.info.update("Loading...")
        self.refresh_info()

    @work(thread=True)
    def refresh_info(self):
        result = subprocess.run(
            ["rye", "list"], capture_output=True, text=True, cwd=Path(".")
        )
        if result.returncode == 0:
            msg = result.stdout
            print(msg)
            self.info.update(f"""{msg}""")
        else:
            self.info.update(f"""{result.stderr}""")


class ProjectList(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Project List"
        yield ListView(
            ListItem(Label("Test"), Button("Edit"), Button("Delete")),
            ListItem(Label("Test1"), Button("Edit1"), Button("Delete")),
        )

        return super().compose()


class ProjectInteraction(Container):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Interaction"

        with Vertical():
            with Horizontal():
                yield Button("New Project")
                yield Button("Add/Remove Packages")
                yield Button("Rye Synch + Update")
            with Horizontal():
                yield Button("Pin Python Version")
                yield Button("Build")
                yield Button("Publish")

        return super().compose()


# TODO
# Collapsibles Infos/Packages
## Rye show
## Rye list
class ProjectPreview(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = "Preview"

        content = open(r"pyproject.toml").read()
        project_infos = Static("[green]Hello[/]\n" + content, expand=True)

        yield project_infos

        return super().compose()
