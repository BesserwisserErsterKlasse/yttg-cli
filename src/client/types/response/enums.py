from enum import StrEnum


class ResponseStatus(StrEnum):
    SUCCESS = 'success'
    CLIENT_ERROR = 'client-error'
    INTERNAL_ERROR = 'internal-error'
    TELEGRAM_ERROR = 'telegram-error'
