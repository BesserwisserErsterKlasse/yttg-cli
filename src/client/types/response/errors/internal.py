from dataclasses import dataclass

from client.types.request import YttgRequest
from client.types.response.base import YttgError


@dataclass(frozen=True, slots=True)
class UnmatchedRequestError(YttgError, constructor=True):
    """Request has no corresponding registered handler."""

    request: YttgRequest
    """Request that has not been matched."""
