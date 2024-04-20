from typing import Iterable

from textual import work, on
from textual.widgets import Input, Static, Switch
from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal

from rye_tui.rye_commands import get_rye_config_values, rye_config_set_command
from rye_tui.constants import CONF_OPT_DICT


class ConfigTab(Container):
    def compose(self) -> Iterable[Widget]:
        with Horizontal():
            with Vertical():
                self.conf_default = ConfigDefault()
                yield self.conf_default
                self.conf_sources = ConfigSources()
                yield self.conf_sources
            with Vertical():
                self.conf_behavior = ConfigBehavior()
                yield self.conf_behavior
                self.conf_proxy = ConfigProxy()
                yield self.conf_proxy
        return super().compose()

    @work(thread=True)
    def on_mount(self):
        self.rye_config = get_rye_config_values()
        # prevent Messages on initial load
        with self.prevent(Switch.Changed):
            self.conf_behavior.load_current(conf_dict=self.rye_config["behavior"])


class ConfigDefault(Container):
    category: str = "default"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()


class ConfigBehavior(Container):
    category: str = "behavior"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        for opt, opt_dict in CONF_OPT_DICT[self.category].items():
            opt_name = Static(opt)
            opt_name.tooltip = opt_dict["tooltip"]
            opt_switch = Switch(value=opt_dict["default"], id=f"{self.category}_{opt}")
            opt_switch.loading = True
            with Horizontal(classes=f"config-{self.category}-container"):
                yield opt_name
                yield opt_switch

        return super().compose()

    def load_current(self, conf_dict):
        for opt, opt_dict in CONF_OPT_DICT[self.category].items():
            opt_switch = self.query_one(f"#{self.category}_{opt}")
            opt_switch.value = conf_dict.get(opt, opt_dict["default"])
            opt_switch.loading = False

    @work(thread=True, exclusive=True)
    @on(Switch.Changed)
    def update_value(event, message):
        message.switch.loading = True
        new_value = str(message.value).lower()
        category, option = message.switch.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        message.switch.loading = False
        msg_color = "green" if new_value == "true" else "red"
        event.notify(
            message=f"{category}.{option} set to [{msg_color}]{new_value}[/]",
            title="Config Updated",
        )


class ConfigSources(Container):
    category: str = "source"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()


class ConfigProxy(Container):
    category: str = "proxy"

    def compose(self) -> Iterable[Widget]:
        self.styles.border = ("heavy", "lightblue")
        self.border_title = self.category
        yield Input(self.category)
        return super().compose()
