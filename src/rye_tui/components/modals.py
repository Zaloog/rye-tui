from typing import Iterable
from pathlib import Path

from textual import on, work
from textual.reactive import reactive
from textual.widget import Widget
from textual.validation import Regex, Function
from textual.screen import ModalScreen
from textual.widgets import (
    Input,
    Switch,
    Button,
    Collapsible,
    Static,
    Label,
    ListView,
    DataTable,
)
from textual.containers import Vertical, Horizontal
from textual.worker import get_current_worker

from rye_tui.utils import (
    rye_command_str_output,
    fill_package_add_table,
    check_underscore,
)
from rye_tui.components.helper_widgets import ProjectListItem, ConfigOptionChanger
from rye_tui.constants import SOURCES_DICT


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
                yield Label("coming soon ...")
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
    def close_modal_init(self):
        self.app.pop_screen()

    @on(Button.Pressed, ".btn-continue")
    async def create_project(self):
        project_path = (Path(self.project_path) / self.project_name).as_posix()
        command = f"rye init {project_path}"
        output_str = await self.async_create_project(command=command)
        self.notify(title="New Project created", message=output_str, timeout=1)

        self.app.cfg.add_project(
            new_project_name=self.project_name, new_project_path=project_path
        )
        self.notify(
            f"[blue]{self.project_name}[/] was added to [b]rye-tui[/b] config",
            title="Project List Updated",
            timeout=1,
        )
        self.app.pop_screen()

        project_list = self.app.query_one(ListView)
        project_list.append(item=ProjectListItem(project_title=self.project_name))
        project_list.index = len(project_list.children)
        project_list.action_select_cursor()

    async def async_create_project(self, command):
        output_str = rye_command_str_output(command=command)
        return output_str


class ModalRyePin(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label(f"Pin Python Version of [blue]{self.app.project['name']}[/]")
            self.pin_input = Input(
                placeholder="enter python version to pin (e.g. 3.11)",
                validators=[Regex(r"^3\.(?:[89]|1[012])$")],
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
            command=f"rye pin {new_python_version}", cwd=self.app.project["path"]
        )

        self.app.pop_screen()
        self.app.query_one(ListView).action_select_cursor()

    @on(Button.Pressed, ".btn-cancel")
    def close_modal_pin(self):
        self.app.pop_screen()

    @on(Input.Changed, "#input_pin_python")
    def disable_buttons(self, message: Input.Changed):
        self.query_one(".btn-continue", Button).disabled = not message.input.is_valid

    @on(Input.Submitted, "#input_pin_python")
    def confirm_input(self):
        self.query_one(".btn-continue").press()


class ModalRyeAdd(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")
    option_flags = reactive([])

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label(
                f"Add packages to your project [blue]{self.app.project['name']}[/]",
            )
            self.pin_input = Input(
                placeholder="enter python package to add",
                # validators=[Regex("^3\.(?:[89]|1[012])$")],
                id="input_add_package",
            )
            self.pin_input.tooltip = "press enter or space to submit"
            with Horizontal():
                yield self.pin_input
                yield Button("--dev", id="option_button_dev", variant="warning")

            # All Dev Options
            with Collapsible(title="Options"):
                yield Label("coming soon")
            #     yield VerticalScroll(*[
            #         Horizontal(Label(flag), Input(f'{flag_type}'))
            #         for flag, flag_type in ADD_OPTIONS_DICT.items()
            #         ])

            self.package_table = DataTable(cursor_type="cell", header_height=2)
            self.package_table.add_column("package", key="package", width=16)
            self.package_table.add_column("version", key="version", width=10)
            self.package_table.add_column("added", key="added", width=6)
            self.package_table.add_column("synced", key="synced", width=6)
            self.package_table.add_column("--dev", key="--dev", width=6)
            self.package_table.add_column("remove", key="remove", width=8)

            # Add present packages
            fill_package_add_table(
                package_table=self.package_table, project_dict=self.app.project
            )

            yield self.package_table

            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button(
                    "continue & sync", variant="success", classes="btn-continue"
                )
                yield Button(
                    "continue & dont sync", variant="error", classes="btn-cancel"
                )
        return super().compose()

    @on(Input.Changed, "#input_add_package")
    @on(Input.Submitted, "#input_add_package")
    def new_package_to_list(self, message):
        current_package = message.value.strip()
        if message.value.endswith(" ") or isinstance(message, Input.Submitted):
            message.input.value = ""

            self.package_table.add_row(
                f"[white]{current_package}[/]",
                "00.00.00",
                ":cross_mark:",
                ":cross_mark:",
                ":cross_mark:",
                "remove",
                key=current_package,
            )
            self.rye_add_package(current_package)

    @on(Button.Pressed, "#option_button_dev")
    def use_dev_flag(self, message: Button.Pressed):
        if "--dev" in self.option_flags:
            self.option_flags.remove("--dev")
            message.button.variant = "warning"

        else:
            self.option_flags.append("--dev")
            message.button.variant = "success"

    @work(thread=True)
    def rye_add_package(self, package):
        flags = " ".join(self.option_flags)
        worker = get_current_worker()
        rye_add_str = rye_command_str_output(
            command=f"rye add {package} {flags}", cwd=self.app.project["path"]
        )
        if rye_add_str.startswith("Initializing"):
            rye_add_str = rye_add_str.split("\n")[-1]

        if rye_add_str.startswith(("Added")):
            self.notify(
                message=rye_add_str.replace(package, f"[green]{package}[/]"),
                title="Package Added",
            )
            package_version = rye_add_str.split()[1].lstrip(package)

            if not worker.is_cancelled:
                self.app.call_from_thread(
                    self.package_table.update_cell,
                    row_key=package,
                    column_key="version",
                    value=package_version,
                )
                self.app.call_from_thread(
                    self.package_table.update_cell,
                    row_key=package,
                    column_key="added",
                    value=":white_check_mark:",
                )
                if "--dev" in self.option_flags:
                    self.app.call_from_thread(
                        self.package_table.update_cell,
                        row_key=package,
                        column_key="--dev",
                        value=":white_check_mark:",
                    )

    @on(DataTable.CellSelected)
    def remove_package(self, event: DataTable.CellSelected):
        row_key = event.cell_key.row_key.value
        col_key = event.cell_key.column_key.value

        is_dev = self.package_table.get_cell(row_key=row_key, column_key="--dev")
        dev_flag = "--dev" if is_dev == ":white_check_mark:" else ""

        if col_key == "remove":
            self.package_table.remove_row(row_key)
            rye_rm_str = rye_command_str_output(
                command=f"rye remove {row_key} {dev_flag}", cwd=self.app.project["path"]
            )
            self.notify(
                title="Package Removed",
                message=rye_rm_str.replace(row_key, f"[red]{row_key}[/]"),
            )

    @on(Button.Pressed, ".btn-continue")
    def add_packages_and_sync(self):
        self.app.pop_screen()
        self.app.query_one("#btn_sync").press()

    @on(Button.Pressed, ".btn-cancel")
    def close_modal_add(self):
        self.app.pop_screen()
        self.app.query_one(ListView).action_select_cursor()


class ModalConfirm(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            yield Label(f"Do you want to delete [blue]{self.app.project['name']}[/]")
            yield Label("This will [red]delete[/] all project files!")
            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button(
                    "delete all files", variant="success", classes="btn-continue"
                )
                yield Button(
                    "remove from config", variant="error", classes="btn-cancel"
                )
        return super().compose()

    @on(Button.Pressed, ".btn-continue")
    def delete_all_files(self):
        self.dismiss(True)
        self.notify(
            f"project [blue]{self.app.project['name']}[/] and all files were deleted",
            title="Project List Updated",
        )

    @on(Button.Pressed, ".btn-cancel")
    def delete_only_config_entry(self):
        self.dismiss(False)
        self.notify(
            f"project [blue]{self.app.project['name']}[/] was removed from config",
            title="Project List Updated",
        )


class ModalNewSource(ModalScreen):
    CSS_PATH: Path = Path("../assets/modal_screens.css")

    def compose(self) -> Iterable[Widget]:
        with Vertical():
            with Horizontal():
                yield Label("Source Name")
                yield Input(
                    placeholder="enter new source name (required, no `_` allowed)",
                    valid_empty=False,
                    validators=[Function(check_underscore)],
                    id="sources_name",
                )

            for conf_option, conf_option_dict in SOURCES_DICT.items():
                yield ConfigOptionChanger(
                    category="sources", option=conf_option, opt_dict=conf_option_dict
                )

            with Horizontal(classes="horizontal-conf-cancel"):
                yield Button(
                    "continue", variant="success", classes="btn-continue", disabled=True
                )
                yield Button("cancel", variant="error", classes="btn-cancel")
        return super().compose()

    @on(Input.Changed, "#sources_name")
    def enable_continue_button(self, message: Input.Changed):
        self.query_one(".btn-continue", Button).disabled = not message.input.is_valid

    @on(Button.Pressed, ".btn-continue")
    def return_source_dict(self):
        new_source_dict = {}

        for input_field in self.query(Input):
            _, option = input_field.id.split("_", maxsplit=1)
            option_value = input_field.value

            new_source_dict[option] = option_value

        switch_widget = self.query_one(Switch)
        _, option = switch_widget.id.split("_", maxsplit=1)
        option_value = switch_widget.value
        new_source_dict[option] = option_value

        self.dismiss(new_source_dict)

    @on(Button.Pressed, ".btn-cancel")
    def close_modal_source(self):
        self.app.pop_screen()
