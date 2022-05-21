from dataclasses import asdict
from pathlib import Path

from arkive.core import Track
from arkive.utils.sanitize import sanitize_name


def format_name(template: str, track: Track):
    fields = asdict(track)
    sanitized_fields = {
        field: sanitize_name(name)
        for field, name in fields.items()
    }
    return template.format_map(sanitized_fields)


def explode_name(source: Path, target: Path, name: str):
    tokens = name.split("/")
    for token in tokens:
        target = target.joinpath(token.strip())
    return target.with_suffix(target.suffix + source.suffix)
