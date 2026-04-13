from dataclasses import dataclass

from client.types.response.base import YttgError
from client.types.response.errors.mixins import LinkErrorMixin


@dataclass(frozen=True, slots=True)
class IllFormedLinkError(LinkErrorMixin, YttgError, constructor=True):
    """Not a valid link provided."""

    pass


@dataclass(frozen=True, slots=True)
class NoResultFoundError(LinkErrorMixin, YttgError, constructor=True):
    """A valid link that does not correspond to any video."""

    pass


@dataclass(frozen=True, slots=True)
class InvalidLanguageError(YttgError, constructor=True):
    """Requested video has no audio in the provided language."""

    language: str
    """Chosen YouTube video language code."""
