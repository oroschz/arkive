from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Track:
    """Stores metadata on a single audio track.
    """
    path: Path
    title: Optional[str]
    album: Optional[str]
    artist: Optional[str]
    genre: Optional[str]
