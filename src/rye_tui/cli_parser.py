import argparse
from rye_tui import __version__


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Usage Options")
    parser.add_argument(
        "--version",
        action="version",
        version=f"rye-tui {__version__}",
    )
    # parser.add_argument(
    #     nargs="?",
    #     choices=["add"],
    #     dest="command",
    #     help="""add current path to rye-tui config to track project""",
    # )
    return parser.parse_args(args)
