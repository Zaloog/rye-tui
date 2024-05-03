from typing import Iterable
from pathlib import Path

from textual import on, work
from textual.widget import Widget
from textual.validation import Regex
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Collapsible, Static, Label
from textual.containers import Vertical, Horizontal

from rye_tui.rye_commands import rye_command_str_output


class ModalRyeInit(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")
    rye_command: str = ""
    rye_home = "C:/Users/grams/Desktop/"
    project_name: str = ""
    project_path: str = ""

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
        self.project_name = self.query_one("#input_new_project").value
        self.project_path = self.query_one("#input_path").value

        if self.project_path == self.rye_home[:-1]:
            self.project_path = ""
            self.query_one("#input_path").value = ""
            self.query_one("#btn_home").variant = "warning"

        if (not self.project_path.endswith("/")) and (self.project_path != ""):
            self.project_path += "/"

        self.rye_command = "rye init"
        self.rye_command += " "
        self.rye_command += f"[blue]{self.project_path}[/]"
        self.rye_command += f"[green]{self.project_name}[/]"

        self.query_one("#preview_rye_command").update(self.rye_command)

    @on(Button.Pressed, "#btn_home")
    def toggle_rye_home(self):
        self.project_path = self.query_one("#input_path").value
        if self.rye_home in self.project_path:
            self.project_path = self.query_one("#input_path").value.lstrip(
                self.rye_home
            )
            self.query_one("#btn_home").variant = "warning"
        else:
            self.project_path = self.rye_home + self.query_one("#input_path").value
            self.query_one("#btn_home").variant = "success"

        self.query_one("#input_path").value = self.project_path

    @on(Button.Pressed, ".btn-cancel")
    def close_modal(self):
        self.app.pop_screen()

    @work(thread=False)
    @on(Button.Pressed, ".btn-continue")
    async def create_project(self):
        self.loading = True
        project_path = (Path(self.project_path) / self.project_name).as_posix()
        command = f"rye init {project_path}"
        output_str = rye_command_str_output(command=command)
        self.notify(title="New Project created", message=output_str)

        self.app.cfg.add_project(
            new_project_name=self.project_name, new_project_path=project_path
        )
        self.notify(
            f"[blue]{self.project_name}[/] was added to [b]rye-tui[/b] config",
            title="Project List Updated",
        )
        self.loading = False
        self.app.pop_screen()
        self.app.query_one("#project_list").update()


class ModalRyePin(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label(f"Pin Python Version of [blue]{self.app.active_project}[/]")
            self.pin_input = Input(
                placeholder="enter python version to pin",
                validators=[Regex("^3\.(?:[89]|1[012])$")],
                id="input_pin_python",
            )
            yield self.pin_input
            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button(
                    "continue", variant="success", classes="btn-continue", disabled=True
                )
                yield Button("cancel", variant="error", classes="btn-cancel")
        return super().compose()

    @on(Button.Pressed, ".btn-continue")
    def pin_new_version(self):
        new_python_version = self.query_one("#input_pin_python").value

        rye_command_str_output(
            command=f"rye pin {new_python_version}", cwd=self.app.active_project_path
        )

        self.app.pop_screen()
        self.app.query_one("#project_list").update()

    @on(Button.Pressed, ".btn-cancel")
    def close_modal(self):
        self.app.pop_screen()

    @on(Input.Changed, "#input_pin_python")
    def disable_buttons(self, event: Input.Changed):
        self.query_one(".btn-continue", Button).disabled = not event.input.is_valid
