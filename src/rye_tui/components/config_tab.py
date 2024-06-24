from typing import Iterable

from textual import work, on
from textual.widgets import Input, Switch, Collapsible, Button, Select
from textual.widget import Widget
from textual.containers import Container, Vertical, Horizontal, VerticalScroll

from rye_tui.utils import (
    get_rye_config_values,
    rye_config_set_command,
    update_rye_config,
)
from rye_tui.constants import CONF_OPT_DICT, SOURCES_DICT
from rye_tui.components.helper_widgets import ConfigOptionChanger
from rye_tui.components.modals import ModalNewSource


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
        with self.prevent(Select.Changed, Switch.Changed, Input.Submitted):
            self.conf_default.load_current(conf_dict=self.rye_config.get("default", {}))
            self.conf_behavior.load_current(
                conf_dict=self.rye_config.get("behavior", {})
            )
            self.conf_proxy.load_current(conf_dict=self.rye_config.get("proxy", {}))
            self.conf_sources.load_current(sources=self.rye_config.get("sources", []))


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

    @work(thread=True, exclusive=True)
    @on(Input.Submitted)
    def update_input_value(self, message: Input.Submitted):
        message.input.loading = True
        new_value = message.value
        category, option = message.input.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        message.input.loading = False

        msg_show = (
            f"set to [green]{new_value}[/]" if new_value else "set to [red]default[/]"
        )
        self.notify(
            message=f"{category}.{option} {msg_show}",
            title="Config Updated",
        )

    @work(thread=True, exclusive=True)
    @on(Select.Changed)
    def update_select_value(self, message: Select.Changed):
        self.log.error("Here")
        message.select.loading = True
        new_value = message.value
        category, option = message.select.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        message.select.loading = False

        self.notify(
            message=f"{category}.{option} set to [green]{new_value}[/]",
            title="Config Updated",
        )


########################################################################################
# Behavior
class ConfigBehavior(VerticalScroll):
    category: str = "behavior"
    default_category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category

        for conf_option, conf_option_dict in self.default_category_dict.items():
            yield ConfigOptionChanger(
                category=self.category, option=conf_option, opt_dict=conf_option_dict
            )

        return super().compose()

    def load_current(self, conf_dict):
        for conf_option, conf_option_dict in self.default_category_dict.items():
            option_widget = self.query_one(f"#{self.category}_{conf_option}")
            option_widget.value = conf_dict.get(
                conf_option, conf_option_dict["default"]
            )

    @work(thread=True, exclusive=True)
    @on(Switch.Changed)
    def update_value(self, message: Switch.Changed):
        message.switch.loading = True
        new_value = str(message.value).lower()
        category, option = message.switch.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        message.switch.loading = False
        msg_color = "green" if new_value == "true" else "red"
        self.notify(
            message=f"{category}.{option} set to [{msg_color}]{new_value}[/]",
            title="Config Updated",
        )


########################################################################################
# Sources
class ConfigSources(VerticalScroll):
    category: str = "sources"
    default_source_list: dict = CONF_OPT_DICT["sources"]
    config_toml: dict = get_rye_config_values()
    source_names_list: list = ["default"]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for source in self.default_source_list:
            with Collapsible(title=source["name"]):
                # loop over url/username/pw/verify-ssl
                for source_option, source_value_dict in SOURCES_DICT.items():
                    yield ConfigOptionChanger(
                        category=f"{self.category}_{source['name']}",
                        option=source_option,
                        opt_dict=source_value_dict,
                    )

        yield Button("Add new Source", id="btn_new_source")
        return super().compose()

    @work()
    async def load_current(self, sources):
        for source in sources:
            with self.prevent(Select.Changed):
                if source["name"] not in self.source_names_list:
                    await self.mount(
                        Collapsible(
                            *[
                                ConfigOptionChanger(
                                    category=f"{self.category}_{source['name']}",
                                    option=source_option,
                                    opt_dict=source_option_dict,
                                )
                                for source_option, source_option_dict in SOURCES_DICT.items()
                            ],
                            title=source["name"],
                        ),
                        before="#btn_new_source",
                    )

                for source_option, source_option_dict in SOURCES_DICT.items():
                    option_widget = self.query_one(
                        f"#{self.category}_{source['name']}_{source_option}"
                    )
                    option_widget.value = source.get(
                        source_option, source_option_dict["default"]
                    )
                self.source_names_list.append(source["name"])

    @work(thread=True, exclusive=True)
    @on(Input.Submitted)
    def update_source_value(self, message: Input.Submitted):
        message.input.loading = True
        new_value = message.value
        category, option = message.input.id.split("_", maxsplit=1)
        source_name, source_option = option.split("_")
        # Update config Toml
        for source in self.config_toml[category]:
            if source["name"] == source_name:
                source[source_option] = new_value

        update_rye_config(conf_dict=self.config_toml)

        message.input.loading = False

        msg_show = (
            f"set to [green]{new_value}[/]" if new_value else "set to [red]default[/]"
        )
        self.notify(
            message=f"{category}.{option} {msg_show}",
            title="Config Updated",
        )

    @work(thread=True, exclusive=True)
    @on(Switch.Changed)
    def update_source_ssl_value(self, message: Switch.Changed):
        message.switch.loading = True
        new_value = str(message.value).lower()
        category, option = message.switch.id.split("_", maxsplit=1)
        source_name, source_option = option.split("_")
        # Update config toml
        for source in self.config_toml[category]:
            if source["name"] == source_name:
                source[source_option] = True if new_value == "true" else False

        update_rye_config(conf_dict=self.config_toml)

        message.switch.loading = False
        msg_color = "green" if new_value == "true" else "red"
        self.notify(
            message=f"{category}.{option} set to [{msg_color}]{new_value}[/]",
            title="Config Updated",
        )

    @on(Button.Pressed, "#btn_new_source")
    def create_new_source(self, message: Button.Pressed):
        # modal for new source
        self.app.push_screen(ModalNewSource(), self.add_new_source)

    def add_new_source(self, new_source_dict: dict) -> None:
        if new_source_dict:
            self.config_toml[self.category].append(new_source_dict)
            update_rye_config(conf_dict=self.config_toml)
            self.load_current(self.config_toml["sources"])


########################################################################################
# Proxy
class ConfigProxy(VerticalScroll):
    category: str = "proxy"
    category_dict: dict = CONF_OPT_DICT[category]

    def compose(self) -> Iterable[Widget]:
        self.classes = "section"
        self.border_title = self.category
        for conf_option, conf_option_dict in self.category_dict.items():
            yield ConfigOptionChanger(
                category=self.category, option=conf_option, opt_dict=conf_option_dict
            )
        return super().compose()

    def load_current(self, conf_dict):
        for conf_option, conf_option_dict in self.category_dict.items():
            option_widget = self.query_one(f"#{self.category}_{conf_option}")
            option_widget.value = conf_dict.get(
                conf_option, conf_option_dict["default"]
            )

    @work(thread=True, exclusive=True)
    @on(Input.Submitted)
    def update_proxy_value(self, message: Input.Submitted):
        message.input.loading = True
        new_value = str(message.value).lower()
        category, option = message.input.id.split("_")
        rye_config_set_command(category=category, option=option, value=new_value)
        message.input.loading = False

        msg_show = f"set to [green]{new_value}[/]" if new_value else "[red]removed[/]"
        self.notify(
            message=f"{category}.{option} {msg_show}",
            title="Config Updated",
        )
