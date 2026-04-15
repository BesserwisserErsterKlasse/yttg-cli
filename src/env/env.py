from typing import ClassVar, Final

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptoSettings(BaseModel):
    pre_shared_secret: bytes
    """Pre-shared secret for public key exchange."""


class Env(BaseSettings):
    crypto: CryptoSettings

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
    )


env: Final[Env] = Env()
"""Environment variables."""
