# Required for AES_GCM_Engine
import os
import io
import json
import six
import cryptography

from base64 import b64encode, b64decode
from cryptography.exceptions import InvalidTag
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes

from sqlalchemy_utils.types.encrypted.encrypted_type import (
    EncryptionDecryptionBaseEngine,
)


class AES_GCM_Engine(EncryptionDecryptionBaseEngine):
    BLOCK_SIZE = 16
    IV_BYTES_NEEDED = 12
    TAG_SIZE_BYTES = BLOCK_SIZE

    def _initialize_engine(self, parent_class_key):
        self.secret_key = parent_class_key

    def encrypt(self, value):
        if not isinstance(value, str):
            value = repr(value)
        if isinstance(value, str):
            value = str(value)
        value = value.encode()
        iv = os.urandom(self.IV_BYTES_NEEDED)
        cipher = Cipher(
            algorithms.AES(self.secret_key), modes.GCM(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(value) + encryptor.finalize()
        # assert len(encryptor.tag) == self.TAG_SIZE_BYTES
        encrypted = b64encode(iv + encryptor.tag + encrypted)
        return encrypted.decode("utf-8")

    def decrypt(self, value):
        if isinstance(value, str):
            value = str(value)
        decrypted = b64decode(value)
        if len(decrypted) < self.IV_BYTES_NEEDED + self.TAG_SIZE_BYTES:
            raise InvalidCiphertextError()
        iv = decrypted[: self.IV_BYTES_NEEDED]
        tag = decrypted[
            self.IV_BYTES_NEEDED : self.IV_BYTES_NEEDED + self.TAG_SIZE_BYTES
        ]
        decrypted = decrypted[self.IV_BYTES_NEEDED + self.TAG_SIZE_BYTES :]
        cipher = Cipher(
            algorithms.AES(self.secret_key),
            modes.GCM(iv, tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        try:
            decrypted = decryptor.update(decrypted) + decryptor.finalize()
        except InvalidTag:
            raise InvalidCiphertextError()
        if not isinstance(decrypted, str):
            try:
                decrypted = decrypted.decode("utf-8")
            except UnicodeDecodeError:
                raise InvalidCiphertextError()
        return decrypted
