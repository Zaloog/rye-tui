from typing import Iterable

from textual import work, on
from textual.events import Mount
from textual.widgets import Label, Input, RichLog
from textual.widget import Widget
from textual.containers import Container, Horizontal, VerticalScroll
from rich.table import Table

from rye_tui.utils import rye_command_str_output, display_installed_tools


class GeneralTab(Container):
    def compose(self) -> Iterable[Widget]:
        self.project_home = Horizontal(classes="section")
        self.project_home.border_title = "Project Home Path"
        self.tools = VerticalScroll(classes="section")
        self.tools.border_title = "Installed Tools"
        self.toolchains = Horizontal(classes="section")
        self.toolchains.border_title = "Python Toolchains"
        with self.project_home:
            yield Label("Project :house:")
            yield Input(self.app.cfg.project_home_path, id="input_project_home_path")
        with self.tools:
            yield RichLog(id="log_tools")
        with self.toolchains:
            yield RichLog(id="log_toolchains")
        return super().compose()

    @work(thread=True)
    def on_mount(self, event: Mount) -> None:
        # tool_str = rye_command_str_output(
        #     "rye tools list --include-version --include-scripts"
        # )
        # tools = tool_str.split("\n")
        # t_table = Table(expand=True)
        # t_table.add_column("Tool")
        # t_table.add_column("Version")
        # t_table.add_column("PyPi")

        # for tool in tools:
        #     t_table.add_row(tool, "version", "path")

        log_tools = self.query_one("#log_tools", RichLog)
        t_table = display_installed_tools()
        self.app.call_from_thread(log_tools.write, t_table, expand=True)

        toolchain_str = rye_command_str_output("rye toolchain list")
        toolchains = toolchain_str.split("\n")
        tc_table = Table(expand=True)
        tc_table.add_column("Toolchain")
        tc_table.add_column("Version")
        tc_table.add_column("Path")

        for tc in toolchains:
            py_str, path = tc.split(" ", maxsplit=1)
            path = path.replace("(", "").replace(")", "")
            python, version = py_str.split("@")
            tc_table.add_row(python, version, path)

        log_toolchains = self.query_one("#log_toolchains", RichLog)
        self.app.call_from_thread(log_toolchains.write, tc_table, expand=True)

        return super()._on_mount(event)

    @on(Input.Submitted)
    def update_home_path(self, event):
        new_path = event.input.value
        self.app.cfg.update_home_path(new_path)
        self.notify(
            message=f"set to [blue]{new_path}[/]",
            title="Project Home Path Updated",
        )
