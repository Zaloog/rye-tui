from typing import Iterable

from textual import on
from textual.widget import Widget
from textual.widgets import Button, Label, ListItem, Header


class RyeHeader(Header):
    def compose(self) -> Iterable[Widget]:
        self._show_clock = True
        self.tall = True
        return super().compose()


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
        project_name = self.parent.project_title
        # TODO confirm button
        # TODO remove folders
        self.app.active_project = ""
        self.app.active_project_path = ""
        self.app.cfg.remove_project(project_name=project_name)

        self.app.query_one("#project_list").update()
        self.app.query_one("#project_preview").update_content()

        self.notify(f"Project [red]{project_name}[/] deleted")


class ProjectListItem(ListItem):
    def __init__(self, project_title: str) -> None:
        self.project_title = project_title
        super().__init__()

    def compose(self) -> Iterable[Widget]:
        yield Label(self.project_title)
        yield EditButton()
        yield DeleteButton()

        return super().compose()
