from rye_tui.tui import RyeTui
from rye_tui.config import check_config_exists, create_init_config


def run():
    if not check_config_exists():
        create_init_config()

    app = RyeTui()
    app.run()


if __name__ == "__main__":
    run()
