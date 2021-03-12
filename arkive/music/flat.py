from pathlib import Path
from tinytag import TinyTag, TinyTagException

from arkive.utility.folder import folder_files, folder_cleanup
from arkive.utility.sanitize import sanitize_name, sanitize_path


def flat_music_file(file: Path, destination: Path):
    song = TinyTag.get(file)

    artist = sanitize_name(song.albumartist)
    album = sanitize_name(song.album)
    title = sanitize_name(song.title)

    new_name = f"{artist} - {album} - {title}{file.suffix}"
    new_path = destination / sanitize_path(Path(new_name))

    file.replace(new_path)


def flat_music_collection(origin: Path, destination: Path):
    for file in folder_files(origin, recurse=True):
        try:
            flat_music_file(file, destination)
        except TinyTagException:
            pass
    folder_cleanup(origin)
