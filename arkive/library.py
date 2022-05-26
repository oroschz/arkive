from pathlib import Path

from arkive.utils.adapter import get_track
from arkive.utils.name import format_name, explode_name
from arkive.utils.sanitize import sanitize_path


def rename_track(fmt: str, path: Path, target: Path):
    track = get_track(path)
    name = format_name(fmt, track)
    path_candidate = explode_name(path, target, name)
    new_path = sanitize_path(path_candidate)
    # Auto-generate parent folders and then rename track file
    new_path.parent.mkdir(parents=True, exist_ok=True)
    path.rename(new_path)


def rename_library(fmt: str, source: Path, target: Path):
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        rename_track(fmt, path, target)
