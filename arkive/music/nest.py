from pathlib import Path
from tinytag import TinyTag, TinyTagException

from arkive.utility.folder import folder_files
from arkive.utility.sanitize import sanitize_name, sanitize_path


def nest_music_file(file: Path, destination: Path):
    song = TinyTag.get(file)

    artist = sanitize_name(song.albumartist)
    album = sanitize_name(song.album)
    title = sanitize_name(song.title)

    final_destination = (destination / artist / album / title).with_suffix(file.suffix)

    sanitized_destination = sanitize_path(final_destination)
    sanitized_destination.parent.mkdir(parents=True, exist_ok=True)

    file.replace(sanitized_destination)


def nest_music_collection(origin: Path, destination: Path):
    for file in folder_files(origin):
        try:
            nest_music_file(file, destination)
        except TinyTagException:
            pass
