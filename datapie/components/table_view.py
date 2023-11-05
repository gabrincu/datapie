from textual.widgets import Static, DataTable, ContentSwitcher, Label
from textual.app import ComposeResult
from rich.console import RenderableType
from rich.text import Text
from textual.binding import Binding
from textual import log


# TODO: implement pagination for the table view
# TODO: Implement modifications on table and apply on save with SQL generation
class TableView(Static):
    BINDINGS = [
        Binding("k", "cursor_up", "Cursor Up", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("l", "cursor_right", "Cursor Right", show=False),
        Binding("h", "cursor_left", "Cursor Left", show=False),
        Binding("v", "switch_cursor", "Switch cursor type", show=False),
        Binding("d", "delete_row", "Delete row", show=False),
    ]

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

    def get_columns(self, cursor):
        columns = [description[0] for description in cursor.description]
        return tuple(columns)

    def action_switch_cursor(self):
        table = self.query_one(DataTable)
        if table.cursor_type == "cell":
            table.cursor_type = "row"
        elif table.cursor_type == "row":
            table.cursor_type = "cell"

    def action_delete_row(self):
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        table.remove_row(row_key)

    def action_cursor_up(self):
        table = self.query_one(DataTable)
        table.action_cursor_up()

    def action_cursor_down(self):
        table = self.query_one(DataTable)
        table.action_cursor_down()

    def action_cursor_right(self):
        table = self.query_one(DataTable)
        table.action_cursor_right()

    def action_cursor_left(self):
        table = self.query_one(DataTable)
        table.action_cursor_left()

    def get_data_table(self):
        table = self.query_one(DataTable)
        return table

    def update_contents(self, query):
        cursor = self.connection.cursor()
        content_switcher = self.query_one(ContentSwitcher)
        try:
            cursor.execute(query)
            table = self.query_one(DataTable)
            table.clear(columns=True)
            columns = self.get_columns(cursor)
            table.add_columns(*columns)
            rows = [row for row in cursor]
            for number, row in enumerate(rows):
                label = Text(str(number + 1), style="#B0FC38 italic")
                table.add_row(*row, label=label)
            if content_switcher.current != "results-table":
                content_switcher.current = "results-table"
            log(table.rows)

        except Exception as e:
            content_switcher.current = "status-label"
            print(f"Error executing SQL: {e}")
