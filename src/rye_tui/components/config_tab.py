from typing import Iterable
from textual.widgets import Input
from textual.widget import Widget
from textual.containers import Container


class ConfigTab(Container):
    def compose(self) -> Iterable[Widget]:
        yield Input("Config")
        return super().compose()
