from dataclasses import dataclass, field

from collections import defaultdict
import subprocess
from pathlib import Path

from rye_tui.constants import RYE_CONFIG_OPTION_DICT


def rye_version() -> str:
    result = subprocess.run(["rye", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.split("\n")[0].split(" ")[1]
        return f"Rye Version: {version}"
    return result.stderr


def rye_package_list(cwd: Path = Path.cwd()) -> str:
    result = subprocess.run(["rye", "list"], capture_output=True, text=True, cwd=cwd)
    if result.returncode == 0:
        packages = result.stdout
        return packages
    return result.stderr


def rye_tools_list(cwd: Path = Path.cwd()) -> str:
    result = subprocess.run(
        ["rye", "tools", "list"], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode == 0:
        packages = result.stdout
        return packages
    return result.stderr


def rye_command_str_output(command: str, cwd: Path = Path.cwd()) -> str:
    result = subprocess.run(command.split(" "), capture_output=True, text=True, cwd=cwd)
    if result.returncode == 0:
        packages = result.stdout.strip()
        return packages
    return result.stderr


def rye_config_get_command(category: str, option: str) -> str:
    return f"rye config --get {category}.{option}"


@dataclass
class RyeConfig:
    config_dict: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))

    def __post_init__(self):
        self.get_config_values()

    def get_config_values(self):
        # Behaviour
        for category, category_options in RYE_CONFIG_OPTION_DICT.items():
            for option in category_options.keys():
                command = rye_config_get_command(category=category, option=option)
                self.config_dict[category][option] = rye_command_str_output(command)
