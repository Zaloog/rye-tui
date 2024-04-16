from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer

from rye_tui.components.mainframe import MainFrame
from rye_tui.rye_commands import rye_version


class RyeTui(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            yield MainFrame()
        return super().compose()

    @work(thread=True)
    def on_mount(self) -> None:
        self.sub_title = rye_version()
