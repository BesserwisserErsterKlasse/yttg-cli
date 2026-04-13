from dataclasses import dataclass
from pathlib import Path

from client.types.request.base import (
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
)
from client.types.request.enums import Stream, YttgCommand


@dataclass(frozen=True, slots=True)
class StreamInfoRequest(
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.GET_STREAMS,
):
    pass


@dataclass(frozen=True, slots=True)
class DownloadRequest(
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.DOWNLOAD,
):
    stream: Stream
    """YouTube stream to download."""

    language: str
    """Preffered language of the audio."""

    folder: Path
    """Folder where to save the file."""

    name: str = '{title}'
    """Local name of the media file."""
