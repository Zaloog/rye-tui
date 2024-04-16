from typing import Iterable
from pathlib import Path
import subprocess

from textual import work, on
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Input, Button, Static


class ProjectTab(VerticalScroll):
    info = Static("TestStatic")

    def compose(self) -> Iterable[Widget]:
        yield Input("Projects")
        yield Button("press")
        yield self.info

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


class ProjectView(VerticalScroll): ...
