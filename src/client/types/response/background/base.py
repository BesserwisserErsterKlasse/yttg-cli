from dataclasses import dataclass

from client.types.response.base import YttgResponse


@dataclass(frozen=True)
class BackgroundResponse(YttgResponse):
    pass
