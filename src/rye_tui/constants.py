from rye_tui import tooltips as tt

CONF_OPT_DICT = {
    "default": {
        "requires-python": {
            "default": ">= 3.8",
            "type": str,
            "tooltip": tt.TT_DEFAULT_REQUIRES_PYTHON,
        },
        "toolchain": {
            "default": "cpython@3.11.1",
            "type": str,
            "tooltip": tt.TT_DEFAULT_TOOLCHAIN,
        },
        "build-system": {
            "default": "hatchling",
            "type": str,
            "tooltip": tt.TT_DEFAULT_BUILD_SYSTEM,
        },
        "license": {"default": "MIT", "type": str, "tooltip": tt.TT_DEFAULT_LICENCE},
        "author": {
            "default": "Full Name <email>",
            "type": str,
            "tooltip": tt.TT_DEFAULT_AUTHOR,
        },
        "dependency-operator": {
            "default": ">=",
            "type": str,
            "tooltip": tt.TT_DEFAULT_DEPENDENCY_OPERATOR,
        },
    },
    "proxy": {
        "http": str,
        "https": str,
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
            "name": str,
            "url": str,
        }
    ],
}
