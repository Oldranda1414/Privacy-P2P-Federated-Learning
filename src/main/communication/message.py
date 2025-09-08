from enum import Enum
from peers import Peer
from datetime import datetime
import json

from communication.encodable import Encodable
from logger import get_logger

logger = get_logger("mess", "mess - %(levelname)s - %(message)s")

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
        try:
            return {
                "type": obj.message_type,
                "sender": Peer.to_dict(obj.sender),
                "receiver": Peer.to_dict(obj.receiver),
                "content": obj.content,
                "timestamp": obj.timestamp.isoformat(),
            }
        except Exception as e:
            logger.error(f"error occurred in to_dict: {e}")
            return {}

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        try:
            message_type = data["type"]
            sender = Peer.from_dict(data["sender"])
            receiver = Peer.from_dict(data["receiver"])
            content = data["content"]
            timestamp = datetime.fromisoformat(data["timestamp"])
            msg = cls(message_type, sender, receiver, content, timestamp)
            return msg
        except Exception as e:
            logger.error(f"error occurred in from_dict: {e}")
            raise e

    @classmethod
    def encode(cls, obj: "Message") -> bytes:
        """Encode to JSON string."""
        try:
            return (json.dumps(cls.to_dict(obj)) + "\n").encode()
        except Exception as e:
            logger.error(f"error occurred in encode: {e}")
            return bytes()

    @classmethod
    def decode(cls, data: bytes) -> "Message":
        """Decode JSON string to instance."""
        try:
            obj = json.loads(data.decode().strip())
            return cls.from_dict(obj)
        except Exception as e:
            logger.error(f"error occurred in decode: {e}")
            raise e

