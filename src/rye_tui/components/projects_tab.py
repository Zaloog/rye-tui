from typing import Iterable
from pathlib import Path
import subprocess

from textual import work, on
from textual.containers import VerticalScroll, Container, Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label, Button, Static, ListView, ListItem


class ProjectTab(VerticalScroll):
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
        yield ListView(
            ListItem(Horizontal(Label("Test"), Button("Edit"))),
            ListItem(Label("Test1")),
        )

        return super().compose()


class ProjectInteraction(Container):
    def compose(self) -> Iterable[Widget]:
        yield Button("New Project")
        yield Button("Interaction2")

        return super().compose()


class ProjectPreview(VerticalScroll):
    def compose(self) -> Iterable[Widget]:
        content = open(r"C:\Users\grams\scoop\persist\rye\config.toml").read()
        project_infos = Static("[green]Hello[/]\n" + content, expand=True)

        yield project_infos

        return super().compose()
