from typing import Iterable

from textual import work, on
from textual.widgets import Input, Switch, Collapsible, Button
from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal, VerticalScroll

from rye_tui.utils import get_rye_config_values, rye_config_set_command
from rye_tui.constants import CONF_OPT_DICT, SOURCES_DICT
from rye_tui.components.helper_widgets import ConfigOptionChanger


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
    async def on_mount(self):
        self.rye_config = get_rye_config_values()
        # prevent Messages on initial load
        with self.prevent(Switch.Changed):
            self.conf_default.load_current(conf_dict=self.rye_config.get("default", {}))
            self.conf_behavior.load_current(
                conf_dict=self.rye_config.get("behavior", {})
            )
            self.conf_proxy.load_current(conf_dict=self.rye_config.get("proxy", {}))


########################################################################################
# Default
class ConfigDefault(VerticalScroll):
    category: str = "default"
    category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for opt, opt_dict in self.category_dict.items():
            yield ConfigOptionChanger(
                category=self.category, option=opt, opt_dict=opt_dict
            )
        return super().compose()

    def load_current(self, conf_dict):
        for opt, opt_dict in self.category_dict.items():
            opt_widget = self.query_one(f"#{self.category}_{opt}")
            opt_widget.value = conf_dict.get(opt, opt_dict["default"])


########################################################################################
# Behavior
class ConfigBehavior(VerticalScroll):
    category: str = "behavior"
    category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for opt, opt_dict in self.category_dict.items():
            yield ConfigOptionChanger(
                category=self.category, option=opt, opt_dict=opt_dict
            )

        return super().compose()

    def load_current(self, conf_dict):
        for opt, opt_dict in self.category_dict.items():
            opt_widget = self.query_one(f"#{self.category}_{opt}")
            opt_widget.value = conf_dict.get(opt, opt_dict["default"])

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


########################################################################################
# Sources
class ConfigSources(VerticalScroll):
    category: str = "sources"
    # category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for source in CONF_OPT_DICT[self.category]:
            with Collapsible(title=source["name"]):
                # loop over url/username/pw/verify-ssl
                for sources_val, sources_val_dict in SOURCES_DICT.items():
                    yield ConfigOptionChanger(
                        category=self.category,
                        option=sources_val,
                        opt_dict=sources_val_dict,
                    )

        yield Button("Add new Source")
        return super().compose()

    def load_current(self, conf_dict): ...


########################################################################################
# Proxy
class ConfigProxy(VerticalScroll):
    category: str = "proxy"
    category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for opt, opt_dict in self.category_dict.items():
            yield ConfigOptionChanger(
                category=self.category, option=opt, opt_dict=opt_dict
            )
        return super().compose()

    def load_current(self, conf_dict):
        for opt, opt_dict in self.category_dict.items():
            opt_widget = self.query_one(f"#{self.category}_{opt}")
            opt_widget.value = conf_dict.get(opt, opt_dict["default"])

    @work(thread=True, exclusive=True)
    @on(Input.Submitted)
    def update_value(self, event):
        event.input.loading = True
        new_value = str(event.value).lower()
        category, option = event.input.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        event.input.loading = False

        msg_show = f"set to [green]{new_value}[/]" if new_value else "[red]removed[/]"
        self.notify(
            message=f"{category}.{option} {msg_show}",
            title="Config Updated",
        )
