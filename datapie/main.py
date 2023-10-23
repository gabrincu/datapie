from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from textual.widgets import Footer, Label, Select, Static, Button, TextArea
from datapie.configuration.config import CSS_MAIN, get_db_connection
from datapie.table_view.table_view import TableView
from datapie.tree_view.tree import DbTree

from typing import Type
from textual.types import CSSPathType
from textual.driver import Driver


class ConfigureForm(Static):
    DB_TYPE_LINES = ["SQLite", "MySQL", "PostgreSQL"]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Configure a database", id="configure-text"),
            Select(
                ((line, line) for line in self.DB_TYPE_LINES),
                prompt="What type of database do you want to connect to?",
                id="database-select",
            ),
            Button("Next", variant="primary", id="next"),
            id="dialog",
        )

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed):
        self.title = str(event.value)


class Datapie(App):
    CSS_PATH = CSS_MAIN + "datapie.tcss"

    def __init__(
        self,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
    ):
        super().__init__(
            driver_class=driver_class, css_path=css_path, watch_css=watch_css
        )
        self.connection = get_db_connection("sqlite", "datapie/chinook.db")

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="e", action="run", description="Execute Query", key_display="E"),
    ]

    def compose(self) -> ComposeResult:
        yield Horizontal(
            DbTree(self.connection),
            Vertical(
                TextArea("", language="sql"),
                TableView(self.connection),
            ),
            id="dialog",
        )
        yield Footer()

    @on(DbTree.ExploreTable)
    def on_explore_table(self, event: DbTree.ExploreTable):
        table_view = self.query_one(TableView)
        table_view.update_contents(event.query)

    def on_key(self, event: events.Key):
        if event.key == "e":
            text_area = self.query_one(TextArea)
            table_view = self.query_one(TableView)
            table_view.update_contents(text_area.text)


if __name__ == "__main__":
    app = Datapie()
    app.run()
