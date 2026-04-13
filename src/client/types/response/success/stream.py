from dataclasses import dataclass
from pathlib import Path

from client.types.request import Stream
from client.types.response.base import YttgResponse


@dataclass(frozen=True, slots=True)
class StreamInfoResponse(YttgResponse, constructor=True):
    streams: list[Stream]
    """YouTube video available streams."""


@dataclass(frozen=True, slots=True)
class DownloadResponse(YttgResponse, constructor=True):
    savepath: Path
    """Path where the file has been saved."""
