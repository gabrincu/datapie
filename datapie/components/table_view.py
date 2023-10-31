from textual.widgets import Static, DataTable, ContentSwitcher, Label
from textual.app import ComposeResult
from rich.console import RenderableType
from rich.text import Text
from textual import events, on


class TableView(Static):
    def __init__(
        self,
        db_connection,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            renderable=renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.connection = db_connection

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="status-label"):
            yield Label("No query has been run yet.", id="status-label")
            yield DataTable(id="results-table")


    def on_mount(self):
        print("Mounting table widget...")
        
    def get_table_data(self, table_name):
        cursor = self.connection.execute(f"select * from {table_name} limit 10")
        return cursor

    def get_columns(self, cursor):
        columns = [description[0] for description in cursor.description]
        return tuple(columns)

    def update_contents(self, query):
        cursor = self.connection.cursor()
        content_switcher = self.query_one(ContentSwitcher)
        try:
            cursor.execute(query)
            print(cursor)
            table = self.query_one(DataTable)
            table.clear(columns=True)
            columns = self.get_columns(cursor)
            table.add_columns(*columns)
            rows = [row for row in cursor]
            for number, row in enumerate(rows):
                label = Text(str(number+1), style="#B0FC38 italic")
                table.add_row(*row, label=label)
            if content_switcher.current != "results-table":
                content_switcher.current = "results-table"

        except Exception as e:
            content_switcher.current = "status-label"
            print(f"Error executing SQL: {e}")


