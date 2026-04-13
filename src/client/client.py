from asyncio import open_connection, StreamReader, StreamWriter
from dataclasses import dataclass, field
from json import dumps, loads
from typing import Any

from client.converter import converter
from client.types import YttgRequest, YttgResponse


@dataclass(slots=True)
class YttgClient:
    __host: str
    __port: int
    __reader: StreamReader = field(init=False)
    __writer: StreamWriter = field(init=False)
    __header_size: int

    def __init__(self, host: str, port: int, header_size: int) -> None:
        self.__host = host
        self.__port = port
        self.__header_size = header_size

    async def start(self) -> None:
        """Start the client."""

        self.__reader, self.__writer = await open_connection(self.__host, self.__port)

    async def send(self, request: YttgRequest) -> None:
        """Send request to the server."""

        unstructured_request: dict[str, object] = converter.unstructure(request)
        raw_request: bytes = f'{request.command}#{dumps(unstructured_request)}'.encode()
        header: bytes = f'{len(raw_request):0>{self.__header_size}}'.encode()
        self.__writer.write(header + raw_request)
        await self.__writer.drain()

    async def receive(self) -> YttgResponse:
        """Wait for a response from the server."""

        header: bytes = await self.__reader.readexactly(self.__header_size)
        body: dict[str, Any] = loads(await self.__reader.readexactly(int(header)))
        factory_name: str = body.pop('response-kind')
        return converter.structure(body, YttgResponse.get_factory(factory_name))
