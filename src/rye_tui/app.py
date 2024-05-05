import sys
from rye_tui.tui import RyeTui
from rye_tui.config import check_config_exists, create_init_config
from rye_tui.cli_parser import parse_args


def main(args):
    if not check_config_exists():
        create_init_config()
        return

    args = parse_args(args=args)
    # if args.command == 'add':
    #     add_cwd_to_config()
    #     return

    app = RyeTui()
    app.run()


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
