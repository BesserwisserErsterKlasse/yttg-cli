from dataclasses import dataclass

from client.types.response.background.base import BackgroundResponse


@dataclass(frozen=True, slots=True)
class DownloadProgressResponse(BackgroundResponse, constructor=True):
    current: int
    """Number of bytes downloaded so far."""

    total: int
    """File size in bytes."""

    @property
    def progress_ratio(self) -> float:
        """Proportion of the file downloaded as a value between `0.0` and `1.0`."""

        return self.current / self.total

    @property
    def is_complete(self) -> bool:
        """Whether the download is completed."""

        return self.current == self.total
