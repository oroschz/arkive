import argparse
from pathlib import Path


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='arkive')

    commands = parser.add_subparsers(dest='cmd')

    show = commands.add_parser('show', help='display actions collection inside a given folder.')
    show.add_argument('folder', type=Path)
    show.add_argument('-c', '--cloud', type=str, metavar='SERVICE', choices=['pcloud'])

    auth = show.add_argument_group('authentication')
    auth.add_argument('-t', '--token', type=str)
    auth.add_argument('-u', '--username', type=str)
    auth.add_argument('-p', '--password', type=str)

    flat = commands.add_parser('flat', help='flatten actions files inside a given folder.')
    flat.add_argument('folder', type=Path)
    flat.add_argument('-o', '--output', type=Path)

    nest = commands.add_parser('nest', help='nesting actions files inside a given folder.')
    nest.add_argument('folder', type=Path)
    nest.add_argument('-o', '--output', type=Path)

    return parser.parse_args()


def music_show(folder: Path):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'

    from arkive.drives.local import LocalDrive
    from arkive.actions.show import show_music_collection
    from arkive.utility.table import make_table

    drive = LocalDrive()
    header, content = show_music_collection(drive, folder)
    table = make_table(header, content)
    print(table)


def music_flat(folder: Path, output: Path = None):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'
    if output:
        assert output.is_dir()
    else:
        output = folder

    from arkive.drives.local import LocalDrive
    from arkive.actions.flat import flat_music_collection
    drive = LocalDrive()

    flat_music_collection(drive, folder, output)


def music_nest(folder: Path, output: Path = None):
    assert folder.exists() and folder.is_dir(), f'\'{folder}\' is not a directory.'
    if output:
        assert output.is_dir()
    else:
        output = folder

    from arkive.drives.local import LocalDrive
    from arkive.actions.nest import nest_music_collection

    drive = LocalDrive()
    nest_music_collection(drive, folder, output)


def cloud_music_show(folder: Path, auth: dict):
    from arkive.drives.pcloud import PCloudDrive
    from arkive.actions.show import show_music_collection
    from arkive.utility.table import make_table

    drive = PCloudDrive(auth)
    header, content = show_music_collection(drive, folder)
    table = make_table(header, content)
    print(table)


def main():
    args = cli()
    if args.cmd == 'show':
        if args.cloud:
            if args.token:
                auth = {'auth': args.token}
            elif args.username and args.password:
                auth = {'username': args.username, 'password': args.password}
            else:
                return
            cloud_music_show(args.folder, auth)
        else:
            music_show(args.folder)
    elif args.cmd == 'flat':
        music_flat(args.folder, args.output)
    elif args.cmd == 'nest':
        music_nest(args.folder, args.output)


if __name__ == '__main__':
    main()
