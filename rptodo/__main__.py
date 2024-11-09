"""RP To-Do entry point scripts."""
# rptodo/__main__.py

from rptodo import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()