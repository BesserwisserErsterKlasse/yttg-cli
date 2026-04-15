from asyncio import open_connection, StreamReader, StreamWriter
from dataclasses import dataclass, field
from hashlib import sha256
from hmac import compare_digest, new
from json import dumps, loads
from os import urandom
from struct import pack, unpack
from typing import Any, Final

from pqcrypto.kem.ml_kem_1024 import (  # type: ignore[import-untyped]
    decrypt,
    generate_keypair,
)

from client.converter import converter
from client.crypto import (
    aes256_ctr_decrypt,
    aes256_ctr_encrypt,
    ClientHello,
    compute_handshake_mac,
    derive_handshake_mac_key,
    KeyMaterial,
    ServerHello,
)
from client.types import YttgRequest, YttgResponse

PAYLOAD_SLICE: Final[slice] = slice(None, -32, None)
MAC_SLICE: Final[slice] = slice(-32, None, None)
SEQUENCE_NUMBER_SLICE: Final[slice] = slice(None, 8, None)
CIPHERTEXT_SLICE: Final[slice] = slice(8, None, None)


@dataclass(slots=True)
class YttgClient:
    __host: str
    __port: int
    __reader: StreamReader = field(init=False)
    __writer: StreamWriter = field(init=False)
    __header_size: int
    __pre_shared_key: bytes
    __keys: KeyMaterial
    __send_sequence_number: int
    __receive_sequence_number: int

    def __init__(self, host: str, port: int, header_size: int, psk: bytes) -> None:
        self.__host = host
        self.__port = port
        self.__header_size = header_size
        self.__pre_shared_key = psk
        self.__send_sequence_number = 0
        self.__receive_sequence_number = 0

    async def start(self) -> None:
        """Establish qost-quantum e2e protected connection."""

        self.__reader, self.__writer = await open_connection(self.__host, self.__port)
        public_key, private_key = generate_keypair()
        client_hello: ClientHello = ClientHello(
            magic=b'YTTG-PQ',
            nonce=urandom(32),
            public_key=public_key,
        )
        raw_client_hello: bytes = dumps(converter.unstructure(client_hello)).encode()
        send_header: bytes = f'{len(raw_client_hello):0>{self.__header_size}}'.encode()
        self.__writer.write(send_header + raw_client_hello)
        await self.__writer.drain()
        receive_header: bytes = await self.__reader.readexactly(self.__header_size)
        raw_server_hello: bytes = await self.__reader.readexactly(int(receive_header))
        server_hello: ServerHello = converter.structure(
            obj=loads(raw_server_hello),
            cl=ServerHello,
        )
        shared_secret: bytes = decrypt(private_key, server_hello.ciphertext)
        handshake_mac_key: bytes = derive_handshake_mac_key(
            shared_secret=shared_secret,
            pre_shared_key=self.__pre_shared_key,
            client_nonce=client_hello.nonce,
            server_nonce=server_hello.nonce,
        )
        expected_handshake_mac: bytes = compute_handshake_mac(
            handshake_mac_key=handshake_mac_key,
            raw_client_hello=raw_client_hello,
            server_nonce=server_hello.nonce,
            ciphertext=server_hello.ciphertext,
        )
        if not compare_digest(expected_handshake_mac, server_hello.handshake_mac):
            raise ValueError('invalid handshake MAC')
        self.__keys = KeyMaterial(
            shared_secret=shared_secret,
            pre_shared_key=self.__pre_shared_key,
            client_nonce=client_hello.nonce,
            server_nonce=server_hello.nonce,
            transcript_hash=sha256(raw_client_hello + raw_server_hello).digest(),
        )

    async def send(self, request: YttgRequest) -> None:
        """Send request to the server."""

        unstructured_request: dict[str, object] = converter.unstructure(request)
        raw_request: bytes = f'{request.command}#{dumps(unstructured_request)}'.encode()
        payload: bytes = pack('>Q', self.__send_sequence_number) + aes256_ctr_encrypt(
            key=self.__keys.client_encryption_key,
            sequence_number=self.__send_sequence_number,
            plaintext=raw_request,
        )
        self.__send_sequence_number += 1
        record_mac: bytes = new(self.__keys.client_mac_key, payload, sha256).digest()
        record: bytes = payload + record_mac
        header: bytes = f'{len(record):0>{self.__header_size}}'.encode()
        self.__writer.write(header + record)
        await self.__writer.drain()

    async def receive(self) -> YttgResponse:
        """Wait for a response from the server."""

        header: bytes = await self.__reader.readexactly(self.__header_size)
        raw: bytes = await self.__reader.readexactly(int(header))
        payload, received_mac = raw[PAYLOAD_SLICE], raw[MAC_SLICE]
        expected_mac: bytes = new(self.__keys.server_mac_key, payload, sha256).digest()
        if not compare_digest(expected_mac, received_mac):
            raise ValueError('Invalid MAC')
        sequence_number: int = unpack('>Q', payload[SEQUENCE_NUMBER_SLICE])[0]
        if sequence_number != self.__receive_sequence_number:
            raise ValueError(f'Wrong sequence number: expected {(
                    self.__receive_sequence_number
                )}, got {sequence_number}')
        plaintext: bytes = aes256_ctr_decrypt(
            key=self.__keys.server_encryption_key,
            sequence_number=sequence_number,
            ciphertext=payload[CIPHERTEXT_SLICE],
        )
        self.__receive_sequence_number += 1
        body: dict[str, Any] = loads(plaintext)
        factory_name: str = body.pop('response-kind')
        return converter.structure(body, YttgResponse.get_factory(factory_name))
