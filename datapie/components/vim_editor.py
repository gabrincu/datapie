from textual.widgets import TextArea
from textual import events
from textual.binding import Binding
from enum import Enum
from textual.reactive import reactive


class Modes(Enum):
    NORMAL = "normal"
    INSERT = "insert"
    VISUAL = "visual"


class VimEditor(TextArea):
    mode = reactive(Modes.NORMAL.value)

    BINDINGS = [
        Binding("j+k", action="switch_mode", description="Switch Mode", show=False),
    ]

    def __init__(
        self,
        text: str = "",
        *,
        language: str | None = None,
        theme: str | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            text=text,
            language=language,
            theme=theme,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.border_title = "Query Editor"
        self.border_subtitle = self.mode.upper()
        self.current_character = ""
        self.previous_character = ""
        self.cursor_blink = False

    def _on_key(self, event: events.Key):
        if self.mode == Modes.NORMAL.value:
            self.current_character = event.character
            if event.key not in ("ctrl+q", "tab"):
                event.prevent_default()
            match event.character:
                case "i":
                    self.mode = Modes.INSERT.value
                case "w":
                    if self.previous_character == "d":
                        self.action_delete_word_right()
                    else:
                        self.action_cursor_word_right()
                case "d":
                    if self.previous_character == "d":
                        self.action_delete_line()
                    else:
                        if self.selected_text != "":
                            self.delete(self.selection.start, self.selection.end)
                case "b":
                    self.action_cursor_word_left()
                case "V":
                    self.action_select_line()
                case "v":
                    self.mode = Modes.VISUAL.value
                case "h":
                    self.move_cursor_relative(columns=-1)
                case "l":
                    self.move_cursor_relative(columns=+1)
                case "j":
                    self.move_cursor_relative(rows=+1)
                case "k":
                    self.move_cursor_relative(rows=-1)
                case "A":
                    self.action_cursor_line_end()
                    self.mode = Modes.INSERT.value
                case "I":
                    self.action_cursor_line_start()
                    self.mode = Modes.INSERT.value

        elif self.mode == Modes.INSERT.value:
            self.current_character = event.character
            match event.key:
                case "k":
                    if self.previous_character == "j":
                        event.prevent_default()
                        self.mode = Modes.NORMAL.value
                        self.action_delete_left()
        self.previous_character = event.character

    def watch_mode(self, new_mode):
        self.border_subtitle = new_mode.upper()
