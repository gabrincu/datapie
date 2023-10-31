from typing import Type

from textual import on
from textual.app import App
from textual.driver import Driver
from textual.types import CSSPathType

from datapie.components.config_screen import DBConfigScreen, ConnectMessage
from datapie.components.main_screen import MainScreen
from datapie.components.connection_picker_screen import ConnectionPicker
from datapie.configuration.config import CSS_MAIN, is_configured
from datapie.database_adapter import DBAdapter


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
        self.connection = None
        self.configured = is_configured()

    def on_mount(self):
        if self.configured is False:
            self.push_screen(DBConfigScreen(name="ConfigScreen"))
        else:
            self.push_screen(ConnectionPicker(name="ConnectionPicker"))

    @on(ConnectMessage)
    def on_connect_message(self, event: ConnectMessage):
        adapter = DBAdapter(
            event.db_type,
            db_name=event.db_name,
            db_username=event.db_username,
            db_password=event.db_password,
            db_host=event.db_host,
        )
        adapter.connect()
        self.connection = adapter.connection
        self.pop_screen()
        self.push_screen(MainScreen(self.connection, name="MainScreen"))


if __name__ == "__main__":
    app = Datapie()
    app.run()
