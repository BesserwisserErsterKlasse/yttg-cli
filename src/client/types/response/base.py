from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from client.types.response.enums import ResponseStatus
from client.utils.case import to_dash_case


@dataclass(frozen=True)
class YttgResponse(ABC):
    kind: ClassVar[str]
    """Response kind."""

    status: ResponseStatus
    """Response status."""

    @staticmethod
    def get_factory(name: str) -> type[YttgResponse]:
        """Retrieve a registered response type by name."""

        return YttgResponse.__response_map[name]

    __response_map: ClassVar[dict[str, type[YttgResponse]]] = {}

    def __init_subclass__(cls, constructor: bool = False) -> None:
        cls.kind = to_dash_case(cls.__name__)
        if constructor:
            cls.__response_map[to_dash_case(cls.__name__)] = cls


@dataclass(frozen=True, slots=True)
class YttgError(YttgResponse, ABC, constructor=False):
    message: str
    """Response error message."""
