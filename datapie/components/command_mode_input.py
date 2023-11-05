from textual.binding import Binding
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Input
from textual.containers import Vertical
from dataclasses import dataclass

import os
import sys
import errno
import enum

ERROR_INVALID_NAME = 123


def is_pathname_valid(pathname: str) -> bool:
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        assert os.path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True


def is_path_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname: str) -> bool:
    try:
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname)
        )
    except OSError:
        return False


@dataclass
class ExportCommand:
    export_path: str = ""


@dataclass
class QuitCommand:
    pass


@dataclass
class WriteCommand:
    pass


class CommandModeBox(ModalScreen):
    BINDINGS = [
        Binding("escape", "close_command_mode", "Close the command mode input"),
        Binding("enter", "execute_command", "Execute the typed command"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Input(placeholder="Command:", id="command_input"), id="command_container"
        )

    def action_close_command_mode(self):
        self.app.pop_screen()

    def on_input_submitted(self):
        self.action_execute_command()

    def action_execute_command(self):
        input = self.query_one(Input)
        command = self.parse_command(input.value)
        self.dismiss(command)

    def parse_command(self, command_text):
        tokens = command_text.split(" ")
        command = None
        match tokens[0]:
            case "export":
                if is_path_exists_or_creatable(tokens[1]):
                    command = ExportCommand(export_path=tokens[1])

            case "q" | "quit":
                command = QuitCommand()

            case "w" | "write": 
                command = WriteCommand()

        return command





