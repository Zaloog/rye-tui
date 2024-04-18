from typing import Iterable

from textual import work
from textual.widgets import Input, Static
from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal

from rye_tui.rye_commands import RyeConfig


class ConfigTab(Container):
    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            with Vertical():
                yield ConfigDefault()
                yield ConfigSources()
            with Vertical():
                self.conf_behavior = ConfigBehaviour()
                yield self.conf_behavior
                yield ConfigProxy()
        return super().compose()

    @work(thread=True)
    def on_mount(self):
        rye_conf = RyeConfig()
        self.conf_dict = rye_conf.config_dict
        self.conf_behavior.query_one(Static).update(
            "\n".join(
                [
                    f"{opt}:{opt_val}"
                    for opt, opt_val in self.conf_dict["behavior"].items()
                ]
            )
        )
        print(self.conf_dict)


class ConfigDefault(Container):
    category: str = "Default"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()


class ConfigBehaviour(Container):
    category: str = "Behavior"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Static(self.category)
        return super().compose()


class ConfigSources(Container):
    category: str = "Source"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()


class ConfigProxy(Container):
    category: str = "Proxy"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()
