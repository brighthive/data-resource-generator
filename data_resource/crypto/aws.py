# Required for AWS_AES_Engine
import aws_encryption_sdk
from aws_encryption_sdk.internal.crypto import WrappingKey
from aws_encryption_sdk.key_providers.raw import RawMasterKeyProvider
from aws_encryption_sdk.identifiers import WrappingAlgorithm, EncryptionKeyType

from sqlalchemy_utils.types.encrypted.encrypted_type import (
    EncryptionDecryptionBaseEngine,
)

from base64 import b64encode, b64decode


class AWS_AES_Engine(EncryptionDecryptionBaseEngine):
    def _update_key(self, key):
        self._initialize_engine(key)

    def _initialize_engine(self, parent_class_key):
        self.secret_key = parent_class_key
        self.kms_kwargs = dict(key_ids=[self.secret_key])
        self.master_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(
            **self.kms_kwargs
        )

    def _set_padding_mechanism(self, padding_mechanism=None):
        self.padding_mechanism = padding_mechanism

    def encrypt(self, value):
        ciphertext, encryptor_header = aws_encryption_sdk.encrypt(
            source=value, key_provider=self.master_key_provider
        )
        b64data = b64encode(ciphertext).decode("utf-8")
        return b64data

    def decrypt(self, value):
        decrypted_bytes, decrypted_header = aws_encryption_sdk.decrypt(
            source=b64decode(value.encode()), key_provider=self.master_key_provider
        )
        cycled_plaintext = decrypted_bytes.decode()
        return cycled_plaintext
