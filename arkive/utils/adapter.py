from pathlib import Path

from tinytag import TinyTag

from arkive.core import Track


def get_track(path: Path) -> Track:
    item = TinyTag.get(path)
    track = Track(
        path=path,
        title=item.title,
        album=item.album,
        artist=item.artist,
        genre=item.genre
    )
    return track
