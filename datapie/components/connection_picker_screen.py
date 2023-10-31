from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Center
from textual.widgets import Label, Select, Button
from datapie.configuration.config import parse_config
from datapie.components.config_screen import ConnectMessage


class ConnectionPicker(Screen):
    def __init__(
        self, name: str | None = None, id: str | None = None, classes: str | None = None
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.connections = parse_config()

    def compose(self) -> ComposeResult:
        with Vertical(id="connection-picker-form"):
            with Center():
                yield Label(
                    "Pick a connection from the ones you saved",
                    id="connection-picker-label",
                )
            with Center():
                yield Select(
                    self.connections,
                    prompt="Choose connection: ",
                    id="connection-picker-select",
                )
            with Center():
                yield Button("Connect", id="connection-picker-button")

    def on_button_pressed(self, event: Button.Pressed):
        select = self.query_one(Select)
        self.post_message(
            ConnectMessage(
                db_type=select.value.get("db_type"),
                db_name=select.value.get("db_name"),
                db_username=select.value.get("db_username"),
                db_password=select.value.get("db_password"),
            )
        )
        # TODO: Handle empty selection
