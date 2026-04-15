from dataclasses import dataclass

from client.types.response.base import YttgResponse


@dataclass(frozen=True, slots=True)
class ChannelInfoResponse(YttgResponse, constructor=True):
    channels: list[str]
    """
    Tags of Telegram channels user has to subscribe to
    in order to use the prodiver.
    """

    def __repr__(self) -> str:
        return f'Required channels:\n\t{(
            '\n\t'.join(f'https://t.me/{tag}' for tag in self.channels)
        )}'


@dataclass(frozen=True, slots=True)
class SubscribeResponse(YttgResponse, constructor=True):
    channels: list[str]
    """Tags of Telegram channels user subscribed to."""

    def __repr__(self) -> str:
        return f'You subscribed to:\n\t{(
            '\n\t'.join(f'https://t.me/{tag}' for tag in self.channels)
        )}'
