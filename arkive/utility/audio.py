from pathlib import Path
from tinytag import TinyTag, TinyTagException

from arkive.utility.sanitize import sanitize_name


def get_file_tags(file: Path):
    try:
        track = TinyTag.get(file)
        tags = (track.albumartist, track.album, track.title)
        return (sanitize_name(tag) for tag in tags)
    except TinyTagException:
        raise AssertionError()
