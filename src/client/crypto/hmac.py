from __future__ import annotations

from hashlib import sha256
from hmac import new
from struct import pack


def hkdf_expand(key: bytes, info: bytes, length: int) -> bytes:
    output: bytearray = bytearray()
    previous_block: bytes = bytes()
    block_index: int = 0
    while len(output) < length:
        previous_block = new(
            key, previous_block + info + bytes([block_index]), sha256
        ).digest()
        output.extend(previous_block)
        block_index += 1
    return bytes(output[:length])


def derive_handshake_mac_key(
    *,
    shared_secret: bytes,
    pre_shared_key: bytes,
    client_nonce: bytes,
    server_nonce: bytes,
) -> bytes:
    key: bytes = new(
        client_nonce + server_nonce,
        shared_secret + pre_shared_key,
        sha256,
    ).digest()
    return hkdf_expand(key=key, info=b'YTTG-PQ-v1|handshake-mac', length=32)


def compute_handshake_mac(
    *,
    handshake_mac_key: bytes,
    raw_client_hello: bytes,
    server_nonce: bytes,
    ciphertext: bytes,
) -> bytes:
    mac_input: bytes = (
        raw_client_hello + server_nonce + pack('>I', len(ciphertext)) + ciphertext
    )
    return new(handshake_mac_key, mac_input, sha256).digest()
