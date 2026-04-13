from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class LinkErrorMixin(ABC):
    link: str
    """Link to the YouTube video."""


@dataclass(frozen=True)
class ProviderErrorMixin(ABC):
    provider: str
    """Tag of the telegram bot that handles the request."""
