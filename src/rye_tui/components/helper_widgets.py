from typing import Iterable

from textual import on
from textual.widget import Widget
from textual.widgets import Button, Label, ListItem


class EditButton(Widget):
    def compose(self) -> Iterable[Widget]:
        yield Button(label="Edit", classes="edit-button", variant="warning")
        return super().compose()


class DeleteButton(Widget):
    def compose(self) -> Iterable[Widget]:
        yield Button(label="Delete", classes="delete-button", variant="error")
        return super().compose()

    @on(Button.Pressed)
    def delete_project(self):
        self.app.log.error(self.parent.project_title)


class ProjectListItem(ListItem):
    def __init__(self, project_title: str) -> None:
        self.project_title = project_title
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Label(self.project_title)
        yield EditButton()
        yield DeleteButton()

        return super().compose()
