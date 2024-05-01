from typing import Iterable

from textual import work
from textual.events import Mount
from textual.widgets import Static, Button
from textual.widget import Widget
from textual.containers import Container


# installed tools/packages
# installed python toolchains
# add new toolchain?
class GeneralTab(Container):
    tools = Static("Test")

    def compose(self) -> Iterable[Widget]:
        yield self.tools
        yield Button("Test1")
        yield Button("Test2")
        return super().compose()

    @work(thread=True)
    def on_mount(self, event: Mount) -> None:
        # self.tools.update(rye_tools_list())
        tool_str = "uncomment to get stuff"
        tool_str += "\n"
        # tool_str += rye_command_str_output('rye tools list')
        # tool_str += '\n'
        # tool_str += rye_command_str_output('rye toolchain list')
        self.tools.update(tool_str)
        return super()._on_mount(event)
