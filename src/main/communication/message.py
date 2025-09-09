from enum import Enum
from datetime import datetime
import json

from peers import Peer
from communication.encodable import Encodable
from logger import get_logger

logger = get_logger("mess", "mess - %(levelname)s - %(message)s")

# TODO remove the HANDSHAKE_ACK type and use contents to distinguish
class MessageType(str, Enum):
    HANDSHAKE = "handshake"
    HANDSHAKE_ACK = "handshakeack"
    POLLING = "polling"
    FSM = "fsm"

class Message(Encodable):
    def __init__(self, message_type: MessageType, sender: Peer, receiver: Peer, content: str, timestamp: datetime):
        self.message_type = message_type
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = timestamp

    @classmethod
    def to_dict(cls, obj: "Message") -> dict:
        return {
            "type": obj.message_type,
            "sender": Peer.to_dict(obj.sender),
            "receiver": Peer.to_dict(obj.receiver),
            "content": obj.content,
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
        return cls.from_dict(obj)

