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

    def __str__(self) -> str:
        return f'{self.title}\n\t' + '\n\t'.join(
            (
                f'Views: {self.views}',
                f'Duration: {self.duration} seconds',
                f'Link: {self.link}',
                f'Thumbnail: {self.thumbnail_link}',
            )
        )


@dataclass(frozen=True, slots=True)
class SearchResponse(YttgResponse, constructor=True):
    offset: str | None
    """Opaque pagination token tied to the search query."""

    videos: list[VideoInfo]
    """YouTube videos matching the query."""

    def __repr__(self) -> str:
        return f'Offset: {self.offset}\n{'\n'.join(map(str, self.videos))}'
