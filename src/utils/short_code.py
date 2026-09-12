from typing import Protocol

import secrets
import string


class ShortCodeGenerator(Protocol):
    def generate(self) -> str: ...


class RandomShortCodeGenerator:
    def __init__(self, length: int = 6):
        self._alphabet = string.ascii_letters + string.digits
        self._length = length

    def generate(self) -> str:
        return "".join(
            secrets.choice(self._alphabet)
            for _ in range(self._length)
        )