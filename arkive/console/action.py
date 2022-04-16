from pathlib import Path


def create_drive(service: str = None, auth: dict = None):
    if not service:
        from arkive.drives.local import LocalDrive
        return LocalDrive()

    if not auth:
        raise AssertionError("Expected auth information.")

    if service == "pcloud":
        from arkive.drives.pcloud import PCloudDrive
        return PCloudDrive(auth)


def music_show(folder: Path, cloud: str = None, auth: dict = None):
    from arkive.actions.show import show_music_collection
    from arkive.utility.table import make_table

    drive = create_drive(cloud, auth)
    header, content = show_music_collection(drive, folder)
    table = make_table(header, content)
    print(table)


def music_flat(folder: Path, output: Path = None, cloud: str = None, auth: dict = None):
    from arkive.actions.flat import flat_music_collection

    if not output:
        output = folder

    drive = create_drive(cloud, auth)
    flat_music_collection(drive, folder, output)


def music_nest(folder: Path, output: Path = None, cloud: str = None, auth: dict = None):
    from arkive.actions.nest import nest_music_collection

    if not output:
        output = folder

    drive = create_drive(cloud, auth)
    nest_music_collection(drive, folder, output)
