from pathlib import Path
from pathvalidate import sanitize_filename, sanitize_filepath


def sanitize_name(name: str) -> str:
    new_name = sanitize_filename(name)
    return str(new_name) or "BLANK"


def sanitize_path(path: Path) -> Path:
    if not isinstance(path, Path):
        raise ValueError
    new_path = sanitize_filepath(path, platform='auto')
    return Path(new_path)


def sanitize_label(label: str, subs: str = "□") -> str:
    if not label.isprintable():
        return "".join(char.isprintable() and char or subs for char in label)
    return label
