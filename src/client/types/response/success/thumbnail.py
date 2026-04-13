from dataclasses import dataclass
from pathlib import Path

from client.types.response.base import YttgResponse


@dataclass(frozen=True, slots=True)
class ThumbnailResponse(YttgResponse, constructor=True):
    savepath: Path
    """Path to the saved thumbnail."""
