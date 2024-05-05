from typing import Iterable
from pathlib import Path

from textual import on, work
from textual.widget import Widget
from textual.validation import Regex
from textual.screen import ModalScreen
from textual.widgets import (
    Input,
    Button,
    Collapsible,
    Static,
    Label,
    ListView,
    RichLog,
    DataTable,
)
from textual.containers import Vertical, Horizontal

from rye_tui.rye_commands import rye_command_str_output
from rye_tui.components.helper_widgets import ProjectListItem


class ModalRyeInit(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")
    rye_command: str = ""
    project_name: str = ""
    project_path: str = ""

    def compose(self) -> Iterable[Widget]:
        self.rye_home = self.app.cfg.project_home_path
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

    @on(Button.Pressed, ".btn-continue")
    async def create_project(self):
        self.loading = True
        project_path = (Path(self.project_path) / self.project_name).as_posix()
        command = f"rye init {project_path}"
        output_str = await self.async_create_project(command=command)
        self.notify(title="New Project created", message=output_str)

        self.loading = False
        self.app.cfg.add_project(
            new_project_name=self.project_name, new_project_path=project_path
        )
        self.notify(
            f"[blue]{self.project_name}[/] was added to [b]rye-tui[/b] config",
            title="Project List Updated",
        )
        self.app.pop_screen()
        project_list = self.app.query_one(ListView)
        project_list.append(item=ProjectListItem(project_title=self.project_name))
        num_project = project_list.children.__len__()
        project_list.index = num_project
        self.app.log.error(num_project)
        project_list.action_select_cursor()

    async def async_create_project(self, command):
        output_str = rye_command_str_output(command=command)
        return output_str


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
        self.app.query_one(ListView).action_select_cursor()

    @on(Button.Pressed, ".btn-cancel")
    def close_modal(self):
        self.app.pop_screen()

    @on(Input.Changed, "#input_pin_python")
    def disable_buttons(self, event: Input.Changed):
        self.query_one(".btn-continue", Button).disabled = not event.input.is_valid

    @on(Input.Submitted, "#input_pin_python")
    def confirm_input(self):
        self.query_one(".btn-continue").press()


class ModalRyeAdd(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")
    packages: list = []

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label(
                f"Add packages to your project [blue]{self.app.active_project}[/]"
            )
            self.pin_input = Input(
                placeholder="enter python package to add",
                # validators=[Regex("^3\.(?:[89]|1[012])$")],
                id="input_add_package",
            )
            yield self.pin_input
            yield RichLog(markup=True, highlight=True)
            self.package_table = DataTable(cursor_type="cell", header_height=2)
            self.package_table.add_column("package", key="package", width=16)
            self.package_table.add_column("version", key="version", width=12)
            self.package_table.add_column("added", key="added", width=6)
            self.package_table.add_column("synced", key="synced", width=6)
            self.package_table.add_column("remove", key="remove", width=14)
            yield self.package_table

            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button("continue", variant="success", classes="btn-continue")
                yield Button("cancel", variant="error", classes="btn-cancel")
        return super().compose()

    @on(Input.Changed, "#input_add_package")
    def new_package_to_list(self, message):
        current_package = message.value.strip()
        if message.value.endswith(" "):
            self.packages.append(current_package)
            message.input.value = ""
            self.query_one(RichLog).write(f"[blue]{current_package}[/]")
            self.package_table.add_row(
                f"[blue]{current_package}[/]",
                "00.00.00",
                # ":white_check_mark:",
                ":cross_mark:",
                ":cross_mark:",
                "remove package",
                key=current_package,
            )
            self.rye_add_package(current_package)

    @work(thread=True)
    def rye_add_package(self, package):
        rye_add_str = rye_command_str_output(
            command=f"rye add {package}", cwd=self.app.active_project_path
        )
        if rye_add_str.startswith("Added"):
            self.notify(
                message=rye_add_str.replace(package, f"[green]{package}[/]"),
                title="Package Added",
            )
            package_version = rye_add_str.split()[1].lstrip(package)
            self.package_table.update_cell(
                row_key=package, column_key="version", value=package_version
            )
            self.package_table.update_cell(
                row_key=package, column_key="added", value=":white_check_mark:"
            )

    @on(DataTable.CellSelected)
    def remove_package(self, event):
        self.log.error(event)
        # Get the keys for the row and column under the cursor.
        row_key = event.cell_key.row_key.value
        col_key = event.cell_key.column_key.value

        self.log.error(row_key, col_key)
        # Supply the row key to `remove_row` to delete the row.
        if col_key == "remove":
            self.package_table.remove_row(row_key)
            rye_rm_str = rye_command_str_output(
                command=f"rye remove {row_key}", cwd=self.app.active_project_path
            )
            self.notify(
                title="Package Removed",
                message=rye_rm_str.replace(row_key, f"[red]{row_key}[/]"),
            )
            self.packages.remove(row_key)

    @on(Button.Pressed, ".btn-continue")
    def pin_new_version(self):
        self.log.error(self.packages)
        # new_python_version = self.query_one("#input_pin_python").value

        # rye_command_str_output(
        #     command=f"rye pin {new_python_version}", cwd=self.app.active_project_path
        # )
        # self.app.pop_screen()

    @on(Button.Pressed, ".btn-cancel")
    def close_modal(self):
        self.app.pop_screen()
