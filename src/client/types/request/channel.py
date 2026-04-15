from dataclasses import dataclass

from client.types.request.base import ProviderRequestMixin, YttgRequest
from client.types.request.enums import YttgCommand


@dataclass(frozen=True, slots=True)
class ChannelInfoRequest(
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.GET_CHANNELS,
    argument_order=['provider'],
):
    pass


@dataclass(frozen=True, slots=True)
class SubscribeRequest(
    ProviderRequestMixin,
    YttgRequest,
    command=YttgCommand.SUBSCRIBE,
    argument_order=['provider', 'channels'],
):
    channels: list[str]
    """Tags of Telegram channels to subscribe to."""
