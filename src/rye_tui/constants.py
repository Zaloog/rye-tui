from pathlib import Path
from platformdirs import user_config_dir

from rye_tui import tooltips as tt

CONFIG_FILE_NAME = "rye-tui.ini"
CONFIG_PATH = Path(
    user_config_dir(appname="rye-tui", appauthor=False, ensure_exists=True)
)
CONFIG_FILE_PATH = CONFIG_PATH / CONFIG_FILE_NAME

IMAGE_PATH = Path(__file__).parent / "static/rye_image.jpg"

CONF_OPT_DICT = {
    "default": {
        "requires-python": {
            "default": ">= 3.8",
            "type": str,
            "tooltip": tt.TT_DEFAULT_REQUIRES_PYTHON,
            "placeholder": "enter python version",
        },
        "toolchain": {
            "default": "cpython@3.11.1",
            "type": str,
            "tooltip": tt.TT_DEFAULT_TOOLCHAIN,
            "placeholder": "enter toolchain",
        },
        "build-system": {
            "default": "hatchling",
            "type": str,
            "tooltip": tt.TT_DEFAULT_BUILD_SYSTEM,
            "placeholder": "enter build-system",
        },
        "license": {"default": "MIT", "type": str, "tooltip": tt.TT_DEFAULT_LICENCE},
        "author": {
            "default": "",
            "type": str,
            "tooltip": tt.TT_DEFAULT_AUTHOR,
            "placeholder": "enter mail to override git",
        },
        "dependency-operator": {
            "default": ">=",
            "type": str,
            "tooltip": tt.TT_DEFAULT_DEPENDENCY_OPERATOR,
        },
    },
    "proxy": {
        "http": {
            "default": "",
            "type": bool,
            "tooltip": tt.TT_PROXY_HTTP,
        },
        "https": {
            "default": "",
            "type": bool,
            "tooltip": tt.TT_PROXY_HTTPS,
        },
    },
    "behavior": {
        "force-rye-managed": {
            "default": False,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_FORCE_RYE_MANAGED,
        },
        "global-python": {
            "default": False,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_GLOBAL_PYTHON,
        },
        "use-uv": {
            "default": False,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_USE_UV,
        },
        "autosync": {
            "default": True,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_AUTOSYNC,
        },
        "venv-mark-sync-ignore": {
            "default": True,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_VENV_MARK_SYNC_IGNORE,
        },
        "fetch-with-build-info": {
            "default": False,
            "type": bool,
            "tooltip": tt.TT_BEHAVIOR_FETCH_WITH_BUILD_INFO,
        },
    },
    "sources": [
        {
            "name": "default",
            "url": "https://pypi.org/simple/",
            "username": "",
            "password": "",
            "verify-ssl": True,
        },
        {
            "name": "test",
            "url": "https://test.pypi.org/simple/",
            "username": "bla",
            "password": "blopb",
            "verify-ssl": True,
        },
    ],
}

OPT_DROPDOWN_DICT = {
    "license": ["MIT", "TEST"],
    "dependency-operator": [">=", "~=", "=="],
}

SOURCES_VALUES = ["url", "username", "password", "verify-ssl"]
