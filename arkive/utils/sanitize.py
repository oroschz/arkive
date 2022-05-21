from pathlib import Path

from pathvalidate import sanitize_filename, sanitize_filepath


def sanitize_name(name: str) -> str:
    new_name = sanitize_filename(name, platform="auto")
    return new_name or "__undefined__"


def sanitize_path(path: Path) -> Path:
    return sanitize_filepath(path, platform="auto")


def ensure_printable(char: str, alt: str):
    if char.isprintable():
        return char
    return alt


def sanitize_output(text: str, alt: str = "□") -> str:
    if text.isprintable():
        return text
    sanitized = (ensure_printable(char, alt) for char in text)
    return "".join(sanitized)


__all__ = ['sanitize_name', 'sanitize_path', 'sanitize_output']
