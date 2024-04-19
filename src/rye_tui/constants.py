# Source: https://rye-up.com/guide/config/#config-file
# Tooltips

TT_BEHAVIOR_FORCE_RYE_MANAGED = """When set to true the `managed` flag is always assumed to be true.
"""
TT_BEHAVIOR_GLOBAL_PYTHON = """Enables global shims when set to `true`.  This means that the installed
`python` shim will resolve to a Rye managed toolchain even outside of
virtual environments.
"""
TT_BEHAVIOR_USE_UV = """When set to `true` enables experimental support of uv as a replacement
for pip-tools. Learn more about uv here: https://github.com/astral-sh/uv
"""
TT_BEHAVIOR_AUTOSYNC = """Enable or disable automatic `sync` after `add` and `remove`.  This defaults
to `true` when uv is enabled and `false` otherwise.
"""
TT_BEHAVIOR_VENV_MARK_SYNC_IGNORE = """Marks the managed .venv in a way that cloud based synchronization systems
like Dropbox and iCloud Files will not upload it.  This defaults to true
as a .venv in cloud storage typically does not make sense.  Set this to
`false` to disable this behavior.
"""
TT_BEHAVIOR_FETCH_WITH_BUILD_INFO = """When set to `true` Rye will fetch certain interpreters with build information.
This will increase the space requirements, will put the interpreter into an
extra folder called `./install/` and place build artifacts adjacent in `./build`.
"""
CONF_OPT_DICT = {
    "default": {
        "requires-python": {"type": str, "default": ""},
        "toolchain": str,
        "build-system": str,
        "license": str,
        "author": str,
        "dependency-operator": str,
    },
    "proxy": {
        "http": str,
        "https": str,
    },
    "behavior": {
        "force-rye-managed": {
            "default": False,
            "type": bool,
            "tooltip": TT_BEHAVIOR_FORCE_RYE_MANAGED,
        },
        "global-python": {
            "default": False,
            "type": bool,
            "tooltip": TT_BEHAVIOR_GLOBAL_PYTHON,
        },
        "use-uv": {
            "default": False,
            "type": bool,
            "tooltip": TT_BEHAVIOR_GLOBAL_PYTHON,
        },
        "autosync": {
            "default": True,
            "type": bool,
            "tooltip": TT_BEHAVIOR_AUTOSYNC,
        },
        "venv-mark-sync-ignore": {
            "default": True,
            "type": bool,
            "tooltip": TT_BEHAVIOR_VENV_MARK_SYNC_IGNORE,
        },
        "fetch-with-build-info": {
            "default": False,
            "type": bool,
            "tooltip": TT_BEHAVIOR_FETCH_WITH_BUILD_INFO,
        },
    },
    "sources": [
        {
            "name": str,
            "url": str,
        }
    ],
}
