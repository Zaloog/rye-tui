from typing import Iterable

from textual import work, on
from textual.events import Mount
from textual.widgets import Label, Input, RichLog
from textual.widget import Widget
from textual.containers import Container, Horizontal

from rye_tui.utils import rye_command_str_output


# installed tools/packages
# installed python toolchains
# add new toolchain?
class GeneralTab(Container):
    def compose(self) -> Iterable[Widget]:
        self.project_home = Horizontal(classes="section")
        self.project_home.border_title = "Project Home Path"
        self.tools = Horizontal(classes="section")
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
        tool_str = rye_command_str_output("rye tools list")
        self.query_one("#log_tools", RichLog).write(tool_str)
        toolchain_str = rye_command_str_output("rye toolchain list")
        self.query_one("#log_toolchains", RichLog).write(toolchain_str)
        return super()._on_mount(event)

    @on(Input.Submitted)
    def update_home_path(self, event):
        new_path = event.input.value
        self.app.cfg.update_home_path(new_path)
        self.notify(
            message=f"set to [blue]{new_path}[/]",
            title="Project Home Path Updated",
        )
