from pyaes import AESModeOfOperationCTR, Counter  # type: ignore[import-untyped]


def aes256_ctr_encrypt(*, key: bytes, sequence_number: int, plaintext: bytes) -> bytes:
    """Encrypt plaintext with AES-256-CTR."""

    counter: Counter = Counter(sequence_number << 64)
    aes: AESModeOfOperationCTR = AESModeOfOperationCTR(key, counter=counter)
    return aes.encrypt(plaintext)  # type: ignore[no-any-return]


def aes256_ctr_decrypt(*, key: bytes, sequence_number: int, ciphertext: bytes) -> bytes:
    """Decrypt ciphertext with AES-256-CTR."""

    counter: Counter = Counter(sequence_number << 64)
    aes: AESModeOfOperationCTR = AESModeOfOperationCTR(key, counter=counter)
    return aes.decrypt(ciphertext)  # type: ignore[no-any-return]
