from textual.widgets import Static, DataTable
from textual.app import ComposeResult
from rich.console import RenderableType


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
        yield DataTable()

    def on_mount(self):
        print("Mounting table widget...")
        table = self.query_one(DataTable)
        table_data = self.get_table_data("artists")
        columns = self.get_columns(table_data)
        table.add_columns(*columns)
        rows = [row for row in table_data]
        table.add_rows(rows)

    def get_table_data(self, table_name):
        cursor = self.connection.execute(f"select * from {table_name} limit 10")
        return cursor

    def get_columns(self, cursor):
        columns = [description[0] for description in cursor.description]
        return tuple(columns)

    def update_contents(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        table = self.query_one(DataTable)
        table.clear(columns=True)
        columns = self.get_columns(cursor)
        table.add_columns(*columns)
        rows = [row for row in cursor]
        table.add_rows(rows)


