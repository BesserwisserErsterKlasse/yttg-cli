from re import compile, Pattern, RegexFlag
from typing import ClassVar, Final

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

IPv4: Final[Pattern[str]] = compile(
    pattern=r'''
        ^(
            localhost
            |
            (?:
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
                \.
                (?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)
            )
        )$
    ''',
    flags=RegexFlag.VERBOSE,
)


class ClientConfig(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra='forbid',
        strict=True,
        validate_default=True,
        json_file='configs/client.json',
    )

    host: str = Field(default='localhost', pattern=IPv4)
    """IP address the client connects to."""

    port: int = Field(default=21027, ge=1024, le=65535)
    """Port which the server listens on."""

    header_size: int = Field(default=16, ge=2)
    """Size in bytes of the YTTG protocol header."""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[
        PydanticBaseSettingsSource,
        JsonConfigSettingsSource,
        PydanticBaseSettingsSource,
        PydanticBaseSettingsSource,
        PydanticBaseSettingsSource,
    ]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


client_config: ClientConfig = ClientConfig()
