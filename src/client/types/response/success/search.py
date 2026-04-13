from dataclasses import dataclass

from client.types.response.base import YttgResponse


@dataclass(frozen=True, slots=True)
class VideoInfo:
    link: str
    """Link to a YouTube video."""

    thumbnail_link: str
    """Link to a YouTube video thumbnail."""

    title: str
    """YouTube video title."""

    duration: int
    """YouTube video duration in seconds."""

    views: str | None
    """Approximate number of views, e.g. `'47M'`"""


@dataclass(frozen=True, slots=True)
class SearchResponse(YttgResponse, constructor=True):
    offset: str | None
    """Opaque pagination token tied to the search query."""

    videos: list[VideoInfo]
    """YouTube videos matching the query."""
