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
