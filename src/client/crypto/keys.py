from dataclasses import dataclass
from hashlib import sha256
from hmac import new

from client.crypto.hmac import hkdf_expand


@dataclass(frozen=True, slots=True)
class KeyMaterial:
    client_encryption_key: bytes
    client_mac_key: bytes
    server_encryption_key: bytes
    server_mac_key: bytes

    def __init__(
        self,
        *,
        shared_secret: bytes,
        pre_shared_key: bytes,
        client_nonce: bytes,
        server_nonce: bytes,
        transcript_hash: bytes,
    ) -> None:
        key: bytes = new(
            client_nonce + server_nonce,
            shared_secret + pre_shared_key,
            sha256,
        ).digest()
        base_info: bytes = b'YTTG-PQ|session|' + transcript_hash
        client_encryption_key: bytes = hkdf_expand(key, base_info + b'|c2s|enc', 32)
        object.__setattr__(self, 'client_encryption_key', client_encryption_key)
        client_mac_key: bytes = hkdf_expand(key, base_info + b'|c2s|mac', 32)
        object.__setattr__(self, 'client_mac_key', client_mac_key)
        server_encryption_key: bytes = hkdf_expand(key, base_info + b'|s2c|enc', 32)
        object.__setattr__(self, 'server_encryption_key', server_encryption_key)
        server_mac_key: bytes = hkdf_expand(key, base_info + b'|s2c|mac', 32)
        object.__setattr__(self, 'server_mac_key', server_mac_key)
