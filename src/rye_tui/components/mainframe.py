from typing import Iterable

from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import TabbedContent, TabPane
from textual.widget import Widget

from rye_tui.components.projects_tab import ProjectTab
from rye_tui.components.general_tab import GeneralTab
from rye_tui.components.config_tab import ConfigTab


class MainFrame(Horizontal):
    BINDINGS = [
        Binding(
            key="ctrl+j",
            action="show_tab('Projects')",
            description="Projects",
            key_display="^j",
            priority=True,
        ),
        Binding(
            key="ctrl+k",
            action="show_tab('General')",
            description="General",
            key_display="^k",
            priority=True,
        ),
        Binding(
            key="ctrl+l",
            action="show_tab('Config')",
            description="Config",
            key_display="^l",
            priority=True,
        ),
    ]

    def compose(self) -> Iterable[Widget]:
        with TabbedContent(initial="Projects"):
            with TabPane("Projects", id="Projects", classes="tabs"):
                yield ProjectTab()
            with TabPane("General", id="General", classes="tabs"):
                yield GeneralTab()
            with TabPane("Config", id="Config", classes="tabs"):
                yield ConfigTab()

        return super().compose()

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab
        self.app.action_focus_next()
