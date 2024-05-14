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


def read_toml(path: str) -> dict:
    try:
        with open(Path(path) / "pyproject.toml", "rb") as tomlfile:
            return tomllib.load(tomlfile)
    except FileNotFoundError:
        return {}


def read_lock(path: str):
    try:
        with open(Path(path) / "requirements.lock", "r") as lockfile:
            packages = [
                line.split("==")[0].strip()
                for line in lockfile.readlines()
                if not line.strip().startswith("#")
            ]
        return [package for package in packages if package]
    except FileNotFoundError:
        return []


def fill_package_table(package_table, project_dict):
    for pkg_str in project_dict["toml"]["project"]["dependencies"]:
        pkg = pkg_str.split("=")[0][:-1]
        version = pkg_str.lstrip(pkg)

        package_table.add_row(
            f"[white]{pkg}[/]",
            version,
            ":white_check_mark:",
            ":white_check_mark:" if pkg in project_dict["lock"] else ":cross_mark:",
            ":cross_mark:",
            "remove",
            key=pkg,
        )
    ...


def prettify_toml(toml_dict):
    for k, v in toml_dict.items():
        print(k)
        print(v)


if __name__ == "__main__":
    prettify_toml(read_toml("."))
