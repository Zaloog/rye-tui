RYE_CONFIG_OPTION_DICT = {
    "default": {
        "requires-python": str,
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
        "force-rye-managed": False,
        "global-python": True,
        "use-uv": True,
        "autosync": False,
        "venv-mark-sync-ignore": True,
        "fetch-with-build-info": False,
    },
    "sources": {
        "default": str,
        "url": str,
    },
}

RYE_CONFIG_TOOLTIP_DICT = {}
