from abc import ABC, abstractmethod
from typing import Type

class Encodable(ABC):
    """Base class for objects that can be serialized for network transfer."""

    @classmethod
    @abstractmethod
    def to_dict(cls, obj) -> dict:
        """Encode to string."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls: Type["Encodable"], data: dict) -> "Encodable":
        """Decode string into an instance."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def encode(cls, obj) -> bytes:
        """Encode to string."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode(cls: Type["Encodable"], data: bytes) -> "Encodable":
        """Decode string into an instance."""
        raise NotImplementedError
