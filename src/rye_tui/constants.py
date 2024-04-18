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
        "force-rye-managed": bool,
        "global-python": bool,
        "use-uv": bool,
        "autosync": bool,
        "venv-mark-sync-ignore": bool,
        "fetch-with-build-info": bool,
    },
    "sources": {
        "default": str,
        "url": str,
    },
}

RYE_CONFIG_TOOLTIP_DICT = {}
