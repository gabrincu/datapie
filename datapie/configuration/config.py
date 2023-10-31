import toml
from enum import Enum
from pathlib import Path
import os

CONFIG_FOLDER = f"{os.environ.get('HOME')}/.config/datapie"
CONFIG_FILE_PATH = f"{CONFIG_FOLDER}/datapie.toml"
CSS_MAIN = "configuration/css/"

Path(CONFIG_FOLDER).mkdir(parents=True, exist_ok=True)


class DBTypes(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    PSQL = "psql"


def get_config():
    toml_data = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as config_file:
            file_contents = config_file.read()
            toml_data = toml.loads(file_contents)
    return toml_data


def create_config(config_data: dict):
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as config_file:
            config_file.write(toml.dumps(config_data))


def is_configured():
    if os.path.exists(CONFIG_FILE_PATH):
        return True
    return False

def parse_config():
    config_data = get_config()
    options = []
    for key, value in config_data.items():
        options.append((key, value))
    return options

    
