from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from client.types.request.enums import YttgCommand


@dataclass(frozen=True, slots=True)
class YttgRequest:
    command: ClassVar[YttgCommand | None] = None
    """Command the request corresponds to."""

    @classmethod
    def get_factory(cls, command: YttgCommand) -> type[YttgRequest]:
        """Get request factory for the given command."""

        if command in cls.__command_map:
            return cls.__command_map[command]
        raise RuntimeError(f'No factory corresponds to \"{command}\" command')

    __command_map: ClassVar[dict[YttgCommand, type[YttgRequest]]] = {}

    def __init_subclass__(cls, command: YttgCommand | None = None) -> None:
        if command is not None:
            cls.command = command
            cls.__command_map[command] = cls


@dataclass(frozen=True)
class LinkRequestMixin(ABC):
    link: str
    """Link to a YouTube video."""


@dataclass(frozen=True)
class ProviderRequestMixin(ABC):
    provider: str
    """Telegram tag of the bot which shall handle the request."""
