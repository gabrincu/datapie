import toml
from pathlib import Path

CONFIG_FILE_PATH = "/Users/gabore/.config/datapie/"
CSS_FILE = "configuration/datapie.css"

Path(CONFIG_FILE_PATH).mkdir(parents=True, exist_ok=True)


def get_config() -> dict:
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        file_contents = config_file.read()
        toml_data = toml.loads(file_contents)

    return toml_data
