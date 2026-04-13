from client.types.response.errors.client import (
    IllFormedLinkError,
    InvalidLanguageError,
    NoResultFoundError,
)
from client.types.response.errors.internal import UnmatchedRequestError
from client.types.response.errors.telegram import (
    InvalidChannelHashError,
    NotSubscribedError,
)

__all__: list[str] = [
    'IllFormedLinkError',
    'InvalidLanguageError',
    'NoResultFoundError',
    'UnmatchedRequestError',
    'InvalidChannelHashError',
    'NotSubscribedError',
]
