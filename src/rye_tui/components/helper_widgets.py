from typing import Iterable

from textual.widget import Widget
from textual.widgets import Button, Label, ListItem, Header, Input, Switch, Static
from textual.containers import Horizontal


class RyeHeader(Header):
    def compose(self) -> Iterable[Widget]:
        self.tall = True
        return super().compose()


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
                placeholder="enter proxy and press enter",
                id=f"{self.category}_{self.option}",
            )
        if self.option_dict["type"] == bool:
            change_widget = Switch(
                value=self.option_dict["default"],
                id=f"{self.category}_{self.option}",
            )

        yield option_name
        yield change_widget

        return super().compose()
