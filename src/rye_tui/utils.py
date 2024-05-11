import tomllib
from shutil import rmtree

import subprocess
from pathlib import Path


def rye_version() -> str:
    result = rye_command_str_output("rye --version")
    version = result.split("\n")[0].split(" ")[1]
    return f"Rye Version: {version}"


def rye_command_str_output(command: str, cwd: str | Path = Path.cwd().as_posix()):
    if isinstance(cwd, str):
        cwd = Path(cwd).as_posix()
    result = subprocess.run(command.split(), capture_output=True, text=True, cwd=cwd)
    if result.returncode == 0:
        packages = result.stdout.strip()
        return packages
    return result.stderr


def rye_config_set_command(category: str, option: str, value=str) -> str:
    if category == "behavior":
        command = f"rye config --set-bool {category}.{option}={value}"
        return rye_command_str_output(command=command)
    if category == "proxy":
        command = f"rye config --set {category}.{option}={value}"
        return rye_command_str_output(command=command)


def get_rye_config_values():
    config_file_path = rye_command_str_output(command="rye config --show-path")
    with open(config_file_path, "rb") as config_file:
        return tomllib.load(config_file)


def delete_folder(folder_path: str | Path):
    rmtree(folder_path)
