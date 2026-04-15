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
    argument_order=['link', 'provider'],
):
    pass


@dataclass(frozen=True, slots=True)
class DownloadRequest(
    LinkRequestMixin,
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.DOWNLOAD,
    argument_order=['link', 'stream', 'language', 'provider', 'folder', 'name'],
):
    stream: Stream
    """YouTube stream to download."""

    folder: Path
    """Folder where to save the file."""

    language: str | None = None
    """Preffered language of the audio."""

    name: str = '{title}'
    """Local name of the media file."""
