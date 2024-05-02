from typing import Iterable
from pathlib import Path

from textual import on
from textual.widget import Widget
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Collapsible, Static, Label
from textual.containers import Vertical, Horizontal


class ModalRyeInit(ModalScreen):
    CSS_PATH = Path("../assets/modal_init.css")
    rye_command: str = "rye init"
    rye_home = "C:User/grams/"

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label("Create a new project")
            yield Input(placeholder="enter project name", id="input_new_project")
            with Horizontal():
                yield Button(":house:", id="btn_home", variant="warning")
                yield Input(placeholder="project path [default: .]", id="input_path")
            with Collapsible(title="other Options"):
                yield Label("Test")
                yield Label("Test2")
            yield Static(self.rye_command, id="preview_rye_command")
            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button("continue", variant="success", classes="btn-continue")
                yield Button("cancel", variant="error", classes="btn-cancel")
        return super().compose()

    @on(Input.Changed)
    def start_new_project(self):
        project_name = self.query_one("#input_new_project").value
        project_path = self.query_one("#input_path").value

        if project_path == self.rye_home[:-1]:
            project_path = ""
            self.query_one("#input_path").value = ""
            self.query_one("#btn_home").variant = "warning"

        if (not project_path.endswith("/")) and (project_path != ""):
            self.app.log.error(repr(project_path))
            project_path += "/"

        command = self.rye_command
        command += " "
        command += f"[blue]{project_path}[/]"
        command += f"[green]{project_name}[/]"

        self.query_one("#preview_rye_command").update(command)

    @on(Button.Pressed, "#btn_home")
    def toggle_rye_home(self):
        project_path = self.query_one("#input_path").value
        if self.rye_home in project_path:
            project_path = self.query_one("#input_path").value.lstrip(self.rye_home)
            self.query_one("#btn_home").variant = "warning"
        else:
            project_path = self.rye_home + self.query_one("#input_path").value
            self.query_one("#btn_home").variant = "success"

        self.query_one("#input_path").value = project_path

    @on(Button.Pressed, ".btn-cancel")
    def close_modal(self):
        self.dismiss()
