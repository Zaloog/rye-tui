import tomlkit
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
    if category in ["proxy", "default"]:
        command = f"rye config --set {category}.{option}={value}"
        return rye_command_str_output(command=command)


def get_rye_config_path() -> str:
    return rye_command_str_output(command="rye config --show-path")


def get_rye_config_values():
    config_file_path = get_rye_config_path()
    return read_toml(path=config_file_path)


def update_rye_config(conf_dict: dict):
    config_file_path = get_rye_config_path()
    save_config_toml(toml_dict=conf_dict, path=config_file_path)


def save_config_toml(toml_dict: dict, path: str) -> None:
    with open(path, "wb") as conf_file:
        conf_file.write(tomlkit.dumps(toml_dict).encode())


def delete_folder(folder_path: str | Path):
    rmtree(folder_path)


def read_toml(path: str) -> dict:
    try:
        toml_path = path if ".toml" in path else Path(path) / "pyproject.toml"
        with open(toml_path, "rb") as tomlfile:
            return tomlkit.load(tomlfile)
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


def display_general_project_infos(path) -> Table:
    try:
        table = Table(
            title="[blue]general[/]",
            show_header=False,
            padding=(0, 0),
            expand=True,
            highlight=True,
        )
        project_infos = rye_command_str_output("rye show", cwd=path).split("\n")

        for pi in project_infos:
            key, val = pi.split(":", maxsplit=1)
            if key == "path":
                table.add_row(key, val)
            elif key == "venv python":
                version = val.split("@")[1]
                table.add_row(key, version)
            elif key == "virtual":
                bool_val = "True" if val == "true" else "False"
                table.add_row(key, bool_val)
        return table
    except Exception:
        return "error getting general info"


def display_toml_project_infos(toml: dict, header: bool = False) -> Table:
    try:
        table = Table(
            title="[blue]toml-file[/]" if header else None,
            show_header=False,
            padding=(0, 0),
            show_edge=True if header else False,
            expand=True,
            highlight=True,
        )

        for k1, v1 in toml.items():
            if isinstance(v1, dict):
                table.add_section()
                val = display_toml_project_infos(toml=v1)
                table.add_row(f"[green]{k1}[/]", val)
            elif isinstance(v1, list):
                table.add_section()
                for i, el in enumerate(v1):
                    if isinstance(el, dict):
                        val = display_toml_project_infos(toml=el)
                    else:
                        val = f"{el}"

                    table.add_row(f"[green]{k1}[/]" if i == 0 else "", val)
            else:
                val = f"{v1}"
                table.add_row(f"[green]{k1}[/]", val)

        return table
    except Exception:
        return "error getting toml info"


def display_package_project_infos(path) -> Table:
    try:
        table = Table(
            title="[blue]installed packages[/]",
            show_header=False,
            padding=(0, 0),
            expand=True,
            highlight=True,
        )
        package_infos = rye_command_str_output("rye list", cwd=path).split("\n")

        for package_str in package_infos:
            try:
                package, version = package_str.split("==")
            except Exception:
                continue
            # if key == "path":
            table.add_row(package, version)

        if table.rows:
            return table
        return "no packages synced yet, add packages and use [blue]rye sync[/]"
    except Exception:
        return "error getting package info with [blue]rye list[/]"


def display_installed_tools() -> Table:
    try:
        table = Table(
            padding=(0, 0),
            expand=True,
            highlight=True,
        )
        table.add_column("Package")
        table.add_column("Version")
        table.add_column("Py Version")
        table.add_column("Scripts")
        tool_str = rye_command_str_output(
            "rye tools list --include-version --include-scripts"
        ).split("\n")

        for tool in tool_str:
            if not tool.startswith(" "):
                command_no = 0
                package, version, pyversion = tool.split(" ")
                pyversion = pyversion.replace("(", "").replace(")", "")
                continue
            else:
                command = tool.strip()
                command_no += 1
                if command_no == 1:
                    table.add_row(package, version, pyversion, command)
                else:
                    table.add_row("", "", "", command)

        if table.rows:
            return table
        return "no tools installed yet"
    except Exception as e:
        print(e)
        return "error getting toml info"


def check_for_rye_project(toml_dict: dict) -> bool:
    if not toml_dict.get("tool", False):
        return False
    return toml_dict.get("tool").get("rye", False)


def check_underscore(s: str) -> bool:
    return "_" not in s
