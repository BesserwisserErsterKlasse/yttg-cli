from enum import StrEnum


class Stream(StrEnum):
    """YouTube video download stream."""

    AUDIO = 'Audio'
    P144 = '144p'
    P240 = '240p'
    P360 = '360p'
    P480 = '480p'
    P720 = '720p'
    P1080 = '1080p'


class YttgCommand(StrEnum):
    DOWNLOAD = 'download'
    GET_CHANNELS = 'get-channels'
    GET_STREAMS = 'get-streams'
    GET_THUMBNAIL = 'get-thumbnail'
    SEARCH = 'search'
    SUBSCRIBE = 'subscribe'
