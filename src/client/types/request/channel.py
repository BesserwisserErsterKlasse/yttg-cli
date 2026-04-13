from dataclasses import dataclass

from client.types.request.base import ProviderRequestMixin, YttgRequest
from client.types.request.enums import YttgCommand


@dataclass(frozen=True, slots=True)
class ChannelInfoRequest(
    ProviderRequestMixin, YttgRequest, command=YttgCommand.GET_CHANNELS
):
    pass


@dataclass(frozen=True, slots=True)
class SubscribeRequest(
    ProviderRequestMixin, YttgRequest, command=YttgCommand.SUBSCRIBE
):
    channels: list[str]
    """Tags of Telegram channels to subscribe to."""
