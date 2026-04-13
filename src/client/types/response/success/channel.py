from dataclasses import dataclass

from client.types.response.base import YttgResponse


@dataclass(frozen=True, slots=True)
class ChannelInfoResponse(YttgResponse, constructor=True):
    channels: list[str]
    """
    Tags of Telegram channels user has to subscribe to
    in order to use the prodiver.
    """


@dataclass(frozen=True, slots=True)
class SubscribeResponse(YttgResponse, constructor=True):
    channels: list[str]
    """Tags of Telegram channels user subscribed to."""
