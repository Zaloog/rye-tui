from typing import Iterable

from textual import work
from textual.events import Mount
from textual.widgets import Static, Button
from textual.widget import Widget
from textual.containers import Container

from rye_tui.rye_commands import rye_tools_list


class GeneralTab(Container):
    tools = Static("Test")

    def compose(self) -> Iterable[Widget]:
        yield self.tools
        yield Button("Test1")
        yield Button("Test2")
        return super().compose()

    @work(thread=True)
    def on_mount(self, event: Mount) -> None:
        self.tools.update(rye_tools_list())
        return super()._on_mount(event)
