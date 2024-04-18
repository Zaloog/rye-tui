from typing import Iterable

from textual.containers import Horizontal
from textual.widgets import TabbedContent, TabPane
from textual.widget import Widget

from rye_tui.components.projects_tab import ProjectTab
from rye_tui.components.general_tab import GeneralTab
from rye_tui.components.config_tab import ConfigTab


class MainFrame(Horizontal):
    def compose(self) -> Iterable[Widget]:
        with TabbedContent(initial="Config"):
            with TabPane("Projects", id="Projects"):
                yield ProjectTab()
            with TabPane("General", id="General"):
                yield GeneralTab()
            with TabPane("Config", id="Config"):
                yield ConfigTab()

        return super().compose()
