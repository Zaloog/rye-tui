import tomllib
from shutil import rmtree

import subprocess
from pathlib import Path
from rich.table import Table


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


def read_lock(path: str, dev: bool):
    try:
        lock_name = "requirements-dev.lock" if dev else "requirements.lock"
        with open(Path(path) / lock_name, "r") as lockfile:
            packages = [
                line.split("==")[0].strip()
                for line in lockfile.readlines()
                if not line.strip().startswith("#")
            ]
        return [package for package in packages if package]
    except FileNotFoundError:
        return []


def fill_package_add_table(package_table, project_dict):
    # packages
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
    # --dev packages
    for pkg_str in project_dict["toml"]["tool"]["rye"]["dev-dependencies"]:
        pkg = pkg_str.split("=")[0][:-1]
        version = pkg_str.lstrip(pkg)

        package_table.add_row(
            f"[white]{pkg}[/]",
            version,
            ":white_check_mark:",
            ":white_check_mark:" if pkg in project_dict["dev_lock"] else ":cross_mark:",
            ":white_check_mark:",
            "remove",
            key=pkg,
        )


def display_project_infos(toml: dict):
    table = Table(
        show_header=False, padding=(0, 0), show_edge=False, expand=True, highlight=True
    )

    for k1, v1 in toml.items():
        if isinstance(v1, dict):
            table.add_section()
            val = display_project_infos(toml=v1)
            table.add_row(f"[green]{k1}[/]", val)
        elif isinstance(v1, list):
            table.add_section()
            for i, el in enumerate(v1):
                # table.show_lines = False if i > 0 else True
                if isinstance(el, dict):
                    val = display_project_infos(toml=el)
                else:
                    val = f"{el}"

                table.add_row(f"[green]{k1}[/]" if i == 0 else "", val)
        else:
            val = f"{v1}"
            table.add_row(f"[green]{k1}[/]", val)

    return table


def prettify_toml(toml_dict):
    for k, v in toml_dict.items():
        print(k)
        print(v)


if __name__ == "__main__":
    prettify_toml(read_toml("."))
