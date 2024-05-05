from typing import Iterable

from textual import work, on
from textual.events import Mount
from textual.widgets import Static, Button, Label, Input
from textual.widget import Widget
from textual.containers import Container, Horizontal


# installed tools/packages
# installed python toolchains
# add new toolchain?
class GeneralTab(Container):
    tools = Static("Test")

    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            yield Label("Project :house:")
            yield Input(self.app.cfg.project_home_path, id="input_project_home_path")
        yield self.tools
        yield Button("Test1")
        yield Button("Test2")
        return super().compose()

    @work(thread=True)
    def on_mount(self, event: Mount) -> None:
        # self.tools.update(rye_tools_list())
        tool_str = "uncomment to get stuff"
        tool_str += "\n"
        tool_str += "Rye Project home"
        tool_str += "\n"
        tool_str += "Rye Tools"
        tool_str += "\n"
        tool_str += "Rye Toolchains"
        # tool_str += rye_command_str_output('rye tools list')
        # tool_str += '\n'
        # tool_str += rye_command_str_output('rye toolchain list')
        self.tools.update(tool_str)
        return super()._on_mount(event)

    @on(Input.Submitted)
    def update_home_path(self, event):
        new_path = event.input.value
        self.app.cfg.update_home_path(new_path)
        self.notify(
            message=f"set to {new_path}",
            title="Project Home Path Updated",
        )
