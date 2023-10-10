from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from datapie.configuration.config import CSS_FILE


class Datapie(App):
    CSS_PATH = CSS_FILE

    def compose(self) -> ComposeResult:
        yield Footer()


if __name__ == "__main__":
    app = Datapie()
    app.run()

