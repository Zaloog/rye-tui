from typing import Iterable

from textual.widget import Widget
from textual.widgets import Button, Label, ListItem, Header, DataTable


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


# Config Widget Line
class ProjectPreviewPackageTable(DataTable):
    def __init__(self, reihe) -> None:
        self.add_rows(reihe)
        super().__init__()
