import configparser

from rye_tui.constants import (
    CONFIG_FILE_NAME,
    CONFIG_FILE_PATH,
    CONFIG_PATH,
)


def create_init_config(conf_path=CONFIG_PATH):
    config = configparser.ConfigParser(default_section=None)
    config.optionxform = str
    config["projects"] = {}

    with open(conf_path / CONFIG_FILE_NAME, "w") as configfile:
        config.write(configfile)


def check_config_exists(path=CONFIG_FILE_PATH):
    return path.exists()


class RyeTuiConfig:
    def __init__(self, path=CONFIG_FILE_PATH) -> None:
        self.configpath = path
        self.config = configparser.ConfigParser(default_section=None)
        self.config.optionxform = str
        self.config.read(path)

    def save(self):
        with open(self.configpath, "w") as configfile:
            self.config.write(configfile)

    @property
    def projects(self) -> str:
        return self.config["projects"]

    def add_project(self, new_project_name, new_project_path) -> None:
        self.config["projects"][new_project_name] = new_project_path
        self.save()

    def remove_project(self, project_name) -> None:
        self.config["projects"].pop(project_name)
        self.save()
