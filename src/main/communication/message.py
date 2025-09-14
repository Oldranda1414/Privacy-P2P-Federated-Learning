from enum import Enum
from datetime import datetime
import json
from typing import Type

from peers import Peer
from communication.encodable import Encodable
from machine_learning.weights import Weights
from logger import get_logger

logger = get_logger("mess")

class MessageType(str, Enum):
    HANDSHAKE = "handshake"
    HANDSHAKE_ACK = "handshakeack"
    HEARTBEAT = "heartbeat"
    SYNC = "sync"
    WEIGHTS = "weights"

_decodable_contents: dict[MessageType, Type[Encodable]] = {
        MessageType.WEIGHTS : Weights
    }

def has_decodeable_contents(message_type: MessageType) -> bool:
    return message_type in _decodable_contents.keys()

def get_contents_type(message_type: MessageType) -> type[Encodable]:
    return _decodable_contents[message_type]

class Message(Encodable):
    def __init__(self, message_type: MessageType, sender: Peer, receiver: Peer, content: str | Encodable, timestamp: datetime):
        self.message_type = message_type
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = timestamp

    @classmethod
    def to_dict(cls, obj: "Message") -> dict:
        content = obj.content
        if not isinstance(content, str):
            content = type(content).to_dict(content)
        return {
            "type": obj.message_type,
            "sender": Peer.to_dict(obj.sender),
            "receiver": Peer.to_dict(obj.receiver),
            "content": content,
            "timestamp": obj.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        message_type = data["type"]
        sender = Peer.from_dict(data["sender"])
        receiver = Peer.from_dict(data["receiver"])
        content = data["content"]
        timestamp = datetime.fromisoformat(data["timestamp"])
        msg = cls(message_type, sender, receiver, content, timestamp)
        return msg

    @classmethod
    def encode(cls, obj: "Message") -> bytes:
        """Encode to JSON string."""
        return (json.dumps(cls.to_dict(obj)) + "\n").encode()

    @classmethod
    def decode(cls, data: bytes) -> "Message":
        """Decode JSON string to instance."""
        obj = json.loads(data.decode().strip())
        message_type = obj["type"]
        if has_decodeable_contents(message_type):
            ContentsType = get_contents_type(message_type)
            obj["content"] = ContentsType.from_dict(obj["content"])
        return cls.from_dict(obj)

