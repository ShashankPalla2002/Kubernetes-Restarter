import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend


class TokenEncryption:
    def __init__(self):
        self._fernet = None
        self._salt = None

    def _get_random_salt(self) -> bytes:
        return os.urandom(16) 

    def _derive_key(self, paraphrase: str, salt: bytes) -> bytes:
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        key = kdf.derive(paraphrase.encode())
        return base64.urlsafe_b64encode(key) 

    def login(self, paraphrase: str, token):
        if self._salt is None:
            self._salt = self._get_random_salt()

        key = self._derive_key(paraphrase, self._salt)
        self._fernet = Fernet(key)
        encryptedToken = self._fernet.encrypt(token.encode())

        self._fernet._signing_key
        return encryptedToken

    # def encryptToken(self, token: str) -> bytes:
    #     if not self._fernet:
    #         raise Exception("You must login first with a paraphrase. kres login")

    #     token = self._fernet.encrypt(token.encode())
    #     return token

    def decryptToken(self, token: bytes) -> str:
        if not self._fernet:
            raise Exception("You must login first with a paraphrase. kres login")

        try:
            return self._fernet.decrypt(token).decode()
        except InvalidToken:
            raise Exception("Invalid paraphrase or corrupted data.")
        
    def deleteKey(self) -> bool:
        if self._fernet:
            del self._fernet
            del self._salt
            self._fernet = None
            self._salt = None

    def status(self) -> bool:
        return self._fernet is not None