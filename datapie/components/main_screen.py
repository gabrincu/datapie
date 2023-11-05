from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer
from textual.binding import Binding
from textual import on

from datapie.components.table_view import TableView
from datapie.components.vim_editor import VimEditor
from datapie.components.tree import DbTree
from datapie.utils import export_to_csv
from datapie.components.command_mode_input import CommandModeBox, ExportCommand, WriteCommand, QuitCommand


class MainScreen(Screen):
    BINDINGS = [
        Binding(key="ctrl+c", action="quit", description="Quit the app"),
        Binding(key="ctrl+e", action="run", description="Execute Query", priority=True),
        Binding(key=":", action="toggle_command", description="Toggle command mode", priority=True),
        # TODO: Make docs screen
        Binding(
            key="question_mark",
            action="help",
            description="Docs",
            key_display="?",
        ),
    ]

    def __init__(
        self,
        db_connection,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.connection = db_connection

    def compose(self) -> ComposeResult:
        yield Horizontal(
            DbTree(self.connection),
            Vertical(
                VimEditor("", language="sql"),
                TableView(self.connection),
            ),
            id="dialog",
        )
        yield Footer()

    @on(DbTree.ExploreTable)
    def on_explore_table(self, event: DbTree.ExploreTable):
        table_view = self.query_one(TableView)
        table_view.update_contents(event.query)

    def action_run(self):
        text_area = self.query_one(VimEditor)
        table_view = self.query_one(TableView)
        if text_area.selected_text != "":
            table_view.update_contents(text_area.selected_text)
        else:
            table_view.update_contents(text_area.text)

    def action_toggle_command(self):
        def run_command(command):
            table = self.query_one(TableView).get_data_table()
            if type(command).__name__ == ExportCommand.__name__:
                export_to_csv(table, command.export_path)
            elif type(command).__name__ == QuitCommand.__name__:
                self.app.exit()
            elif type(command).__name__ == WriteCommand.__name__:
                print("Writing table Diff to DB..")


        self.app.push_screen(CommandModeBox(), run_command)


