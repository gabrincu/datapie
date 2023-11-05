from mysql.connector import Connect
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical, Center, Horizontal
from textual.widgets import Select, Label, ContentSwitcher, Input, Static, Button
from textual.message import Message
from textual import on

from datapie.configuration.config import create_config, DBTypes


class ConnectMessage(Message):
    bubble = True

    def __init__(
        self, db_type, db_name=None, db_username=None, db_password=None, db_host=None
    ) -> None:
        super().__init__()
        self.db_type = db_type
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_host = db_host


class SQLiteForm(Static):
    def compose(self) -> ComposeResult:
        with Vertical(id="sqlite-form-container"):
            with Center():
                yield Label("Enter sqlite db path", id="sqlite-form-label")
            with Center():
                yield Input(
                    placeholder="Name to store connection with",
                    id="sqlite-form-connection-name-input",
                )
            with Center():
                yield Input(
                    placeholder="SQLite DB File Path", id="sqlite-form-path-input"
                )
            with Center():
                yield Button("Connect", id="sqlite-form-connect-button")
                yield Button("Save Config", id="sqlite-form-save-button")

    def on_button_pressed(self, event: Button.Pressed):
        sqlite_path_input = self.query_one("#sqlite-form-path-input", Input)
        #TODO: handle empty Inputs (Try Textual validators)
        if event.button.id == "sqlite-form-save-button":
            connection_name_input = self.query_one(
                "#sqlite-form-connection-name-input", Input
            )
            #TODO: Check for connection existence
            config_data = {
                f"{connection_name_input.value}": {
                    "db_type": DBTypes.SQLITE.value,
                    "db_name": f"{sqlite_path_input.value}",
                }
            }
            create_config(config_data)
        elif event.button.id == "sqlite-form-connect-button":
            self.post_message(
                ConnectMessage(
                    db_type=DBTypes.SQLITE.value, db_name=sqlite_path_input.value
                )
            )

# TODO: Configure this as well
class PSQLForm(Static):
    def compose(self) -> ComposeResult:
        with Vertical(id="psql-form-container"):
            with Center():
                yield Label("Enter PSQL Connection details", id="psql-form-label")
            with Center():
                yield Input(placeholder="DB Host", id="psql-form-host-input")
            with Center():
                yield Input(placeholder="DB Name", id="psql-form-name-input")
            with Center():
                yield Input(placeholder="Username", id="psql-form-username-input")
            with Center():
                yield Input(
                    placeholder="Password", password=True, id="psql-form-password-input"
                )
            with Center():
                with Horizontal():
                    yield Button("Connect", id="psql-form-connect-button")
                    yield Button("Save Config", id="psql-form-save-button")


# TODO: Configure this as well
class MySQLForm(Static):
    class MySQLConnectMessage(Message):
        pass

    def compose(self) -> ComposeResult:
        with Vertical(id="mysql-form-container"):
            with Center():
                yield Label("Enter MySQL Connection details", id="mysql-form-label")
            with Center():
                yield Input(placeholder="DB Host", id="mysql-form-host-input")
            with Center():
                yield Input(placeholder="DB Name", id="mysql-form-name-input")
            with Center():
                yield Input(placeholder="Username", id="mysql-form-username-input")
            with Center():
                yield Input(
                    placeholder="Password",
                    password=True,
                    id="mysql-form-password-input",
                )
            with Center():
                with Horizontal(id="mysql-form-button-container"):
                    with Center():
                        yield Button("Connect", id="mysql-form-connect-button")
                    with Center():
                        yield Button("Save Config", id="mysql-form-save-button")


class DBConfigScreen(Screen):
    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.db_options = [("MySQL", "mysql"), ("PSQL", "psql"), ("SQLite", "sqlite")]
        self.db_type = None

    def compose(self) -> ComposeResult:
        with Vertical(id="db-type-form"):
            yield Label("Select the type of DB you want to connect to.")
            yield Select(self.db_options)
            with ContentSwitcher(initial="placeholder-label", id="config-switcher"):
                yield Label("", id="placeholder-label")
                yield SQLiteForm(id="sqlite-form")
                yield MySQLForm(id="mysql-form")
                yield PSQLForm(id="psql-form")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed):
        self.db_type = event.value
        content_switcher = self.query_one(ContentSwitcher)
        form = self.determine_current(event.value)
        content_switcher.current = form

    def determine_current(self, value):
        return f"{value}-form"
