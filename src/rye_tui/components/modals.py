from typing import Iterable
from pathlib import Path

from textual import on
from textual.widget import Widget
from textual.screen import ModalScreen
from textual.widgets import Input, Button
from textual.containers import Vertical, Horizontal


class ModalRyeInit(ModalScreen):
    CSS_PATH = Path("../assets/modal_init.css")

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Input(placeholder="enter project name", id="input_new_project")
            with Horizontal():
                yield Button(":house:", id="btn_home")
                yield Input(placeholder="project path [default: .]", id="input_path")
            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button("continue", variant="success", classes="btn-continue")
                yield Button("cancel", variant="error", classes="btn-cancel")
        return super().compose()

    @on(Button.Pressed)
    def close_modal(self):
        self.dismiss()
