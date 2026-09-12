from typing import Protocol

from pwdlib import PasswordHash


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed_password: str) -> bool: ...


class Argon2PasswordHasher:
    def __init__(self):
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._password_hash.verify(password, hashed_password)