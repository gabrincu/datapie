import toml
from enum import Enum
from pathlib import Path
import os
import sqlite3

CONFIG_FILE_PATH = "/Users/gabore/.config/datapie/datapie.toml"
CSS_MAIN = "configuration/css/"

Path(CONFIG_FILE_PATH).mkdir(parents=True, exist_ok=True)


class DBTypes(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    PSQL = "PSQL"


def get_config():
    toml_data = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            file_contents = config_file.read()
            toml_data = toml.loads(file_contents)
    return toml_data


def create_config(config_data: dict):
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            config_file.write(toml.dumps(config_data))


def get_db_connection(db_type: str, db_name: str):
    connection = None
    if db_type == DBTypes.SQLITE.value:
        connection = sqlite3.connect(db_name)
    return connection

