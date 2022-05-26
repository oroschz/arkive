from argparse import ArgumentParser
from pathlib import Path

from arkive import __version__
from arkive.library import rename_library


def nest_command(source: Path, output: Path = None, **_):
    if source.exists():
        fmt = "{artist}/{album}/{title}"
        rename_library(fmt, source, output or source)


def flat_command(source: Path, output: Path = None, **_):
    if source.exists():
        fmt = "{artist} - {album} - {title}"
        rename_library(fmt, source, output or source)


def fmt_command(source: Path, output: Path, template: str, **_):
    if source.exists():
        rename_library(template, source, output or source)


def runner(args):
    parser = ArgumentParser(prog="arkive")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    commands = parser.add_subparsers(dest="cmd", title="commands", metavar="<command>")

    flat = commands.add_parser("flat", help="Creates a flat folder structure.")
    flat.add_argument("source", type=Path, help="Folder of your library.")
    flat.add_argument("-o", "--output", type=Path, help="Target folder of your library.")
    flat.set_defaults(call=flat_command)

    nest = commands.add_parser("nest", help="Creates a nested folder structure.")
    nest.add_argument("source", type=Path, help="Folder of your library.")
    nest.add_argument("-o", "--output", type=Path, help="Target folder of your library.")
    nest.set_defaults(call=nest_command)

    fmt = commands.add_parser("fmt", help="Creates a custom filename structure.")
    fmt.add_argument("source", type=Path, help="Folder of your library.")
    fmt.add_argument("-o", "--output", type=Path, help="Target folder of your library.")
    fmt.add_argument("template", type=str, help="Format to define the output filenames.")
    fmt.set_defaults(call=fmt_command)

    options = parser.parse_args(args)
    if "call" not in options:
        parser.print_help()
        return

    options.call(**options.__dict__)
