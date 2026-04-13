from dataclasses import dataclass

from client.types.response.base import YttgError
from client.types.response.errors.mixins import ProviderErrorMixin


@dataclass(frozen=True, slots=True)
class NotSubscribedError(ProviderErrorMixin, YttgError, constructor=True):
    """Telegram user not subscribed to channels required by the provider."""

    pass


@dataclass(frozen=True, slots=True)
class InvalidChannelHashError(YttgError, constructor=True):
    """Channel hash is invalid."""

    channel: str
    """Tag of an invalid channel."""
