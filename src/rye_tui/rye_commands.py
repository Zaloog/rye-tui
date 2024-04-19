import tomllib

import subprocess
from pathlib import Path


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
    result = subprocess.run(command.split(), capture_output=True, text=True, cwd=cwd)
    if result.returncode == 0:
        packages = result.stdout.strip()
        return packages
    return result.stderr


def rye_config_set_command(category: str, option: str, value=str) -> str:
    if category == "behavior":
        command = f"rye config --set-bool {category}.{option}={value}"
        return rye_command_str_output(command=command)


def get_rye_config_values():
    config_file_path = rye_command_str_output(command="rye config --show-path")
    with open(config_file_path, "rb") as config_file:
        return tomllib.load(config_file)
