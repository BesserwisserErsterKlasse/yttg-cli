from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import NoReturn

from cli.aprint import aprint
from cli.parse import parse_command
from client import YttgClient
from client.types import YttgRequest, YttgResponse

type CliCallback = Callable[[YttgResponse], Awaitable[None]]
type Handler[Request: YttgRequest] = Callable[[Request], Awaitable[None]]
type HandlerDecorator[Request: YttgRequest] = Callable[
    [Handler[Request]], Handler[Request]
]


@dataclass(slots=True)
class YttgCli:
    __client: YttgClient
    __callback: CliCallback

    async def start(self) -> NoReturn:
        """Start the CLI."""

        while True:
            try:
                request: YttgRequest = parse_command(command=input('user> '))
            except ValueError as exception:
                print(exception.args[0])
            except Exception as exception:
                print(exception)
            else:
                await self.__client.send(request)
                response: YttgResponse = await self.__client.receive()
                await self.__callback(response)

    def __init__(self, client: YttgClient, callback: CliCallback = aprint) -> None:
        self.__client = client
        self.__callback = callback
