import configparser
from rich.console import Console

from rye_tui.constants import (
    CONFIG_FILE_NAME,
    CONFIG_FILE_PATH,
    CONFIG_PATH,
    PROJECT_HOME_PATH,
)


def create_init_config(conf_path=CONFIG_PATH):
    config = configparser.ConfigParser(default_section=None)
    config.optionxform = str
    config["general"] = {"project_home_path": PROJECT_HOME_PATH}
    config["projects"] = {}

    console = Console(log_path=False)

    console.log('Thank you for using "rye-tui".')
    with open(conf_path / CONFIG_FILE_NAME, "w") as configfile:
        config.write(configfile)
    console.log(
        'Since this is your first time using "rye-tui" a Configuration-File was created [green]successfully[/].'
    )
    console.log('You can now use "trye" again to start working with rye-tui.')


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
    def project_home_path(self) -> str:
        return self.config["general"]["project_home_path"]

    @property
    def projects(self) -> str:
        return self.config["projects"]

    @property
    def project_paths(self) -> str:
        return list(self.config["projects"].values())

    @property
    def project_names(self) -> str:
        return list(self.config["projects"].keys())

    def add_project(self, new_project_name, new_project_path) -> None:
        self.config["projects"][new_project_name] = new_project_path
        self.save()

    def remove_project(self, project_name) -> None:
        self.config["projects"].pop(project_name)
        self.save()

    def update_home_path(self, new_home_path) -> None:
        self.config["general"]["project_home_path"] = new_home_path
        self.save()
