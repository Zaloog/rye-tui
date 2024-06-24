from typing import Iterable

from textual.widget import Widget
from textual.widgets import (
    Button,
    Label,
    ListItem,
    Header,
    Input,
    Switch,
    Static,
    Select,
    LoadingIndicator,
)
from textual.containers import Horizontal, Vertical


class RyeHeader(Header):
    def compose(self) -> Iterable[Widget]:
        self.tall = True
        return super().compose()


class SyncButton(Button):
    def get_loading_widget(self):
        return CustomLoading(text="Syncing...")

    def compose(self) -> Iterable[Widget]:
        self.label = "Rye Sync"
        self.id = "btn_sync"
        return super().compose()


class BuildButton(Button):
    def get_loading_widget(self):
        return CustomLoading(text="Building...")

    def compose(self) -> Iterable[Widget]:
        self.label = "Build"
        self.id = "btn_build"
        return super().compose()

    # def update_label():
    #     for build_file in Path()
    #     if version('rye tiu')

    #     ...


class EditButton(Widget):
    def compose(self) -> Iterable[Widget]:
        yield Button(
            label=":hammer_and_wrench:  Edit",
            classes="edit-button invisible",
            variant="warning",
        )
        return super().compose()


class DeleteButton(Widget):
    def compose(self) -> Iterable[Widget]:
        yield Button(
            label=":cross_mark: Delete",
            classes="delete-button invisible",
            variant="error",
        )
        return super().compose()


class ProjectListItem(ListItem):
    def __init__(self, project_title: str) -> None:
        self.project_title = project_title
        super().__init__(id=project_title)

    def compose(self) -> Iterable[Widget]:
        yield Label(self.project_title)
        yield EditButton()
        yield DeleteButton()

        return super().compose()


class ConfigOptionChanger(Horizontal):
    def __init__(self, category: str, option: str, opt_dict: dict) -> None:
        self.category = category
        self.option = option
        self.option_dict = opt_dict
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        option_name = Static(self.option)
        option_name.tooltip = self.option_dict["tooltip"]

        if self.option_dict["type"] == str:
            change_widget = Input(
                value=self.option_dict["default"],
                placeholder=self.option_dict["placeholder"],
                id=f"{self.category}_{self.option}",
            )
        if self.option_dict["type"] == bool:
            with self.prevent(Select.Changed):
                change_widget = Switch(
                    value=self.option_dict["default"],
                    id=f"{self.category}_{self.option}",
                )
        if self.option_dict["type"] == list:
            with self.prevent(Select.Changed):
                change_widget = Select(
                    # value=Select.BLANK,
                    value=self.option_dict["default"],
                    options=[(opt, opt) for opt in self.option_dict["options"]],
                    allow_blank=False,
                    id=f"{self.category}_{self.option}",
                )

        yield option_name
        yield change_widget

        return super().compose()


class CustomLoading(Vertical):
    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__()

    def compose(self):
        yield Label(self.text)
        yield LoadingIndicator()
