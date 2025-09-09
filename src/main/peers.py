import json
import os

from environment import get_self_id
from communication.encodable import Encodable

class Peer(Encodable):
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port

    def __hash__(self):
        return hash((self.node_id, self.host, self.port))

    def __eq__(self, other):
        if not isinstance(other, Peer):
            return False
        return (self.node_id == other.node_id and 
                self.host == other.host and 
                self.port == other.port)

    @classmethod
    def to_dict(cls, obj: "Peer") -> dict:
        return {
            "node_id": obj.node_id,
            "host": obj.host,
            "port": obj.port,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Peer":
        return cls(data["node_id"], data["host"], data["port"])

    @classmethod
    def encode(cls, obj: "Peer") -> bytes:
        """Encode to JSON string."""
        return json.dumps(cls.to_dict(obj)).encode()

    @classmethod
    def decode(cls, data: bytes) -> "Peer":
        """Decode JSON string to instance."""
        obj = json.loads(data.decode().strip())
        return cls.from_dict(obj)

def load_self(peers_file: str) -> Peer:
    self_id = get_self_id()
    peers = _load_peer_file(peers_file)
    return peers.pop(self_id)

def load_peers(peers_file: str) -> dict[str, Peer]:
    self_id = get_self_id()
    peers = _load_peer_file(peers_file)
    peers.pop(self_id)
    return peers

def _load_peer_file(path: str) -> dict[str, Peer]:
    # look for file in this scipts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    peers_file = os.path.join(script_dir, path)
    
    with open(peers_file, 'r') as f:
        data = json.load(f)
    
    raw_peers = data.get('peers', [])
    return {peer['node_id']: Peer(peer['node_id'], peer['host'], int(peer['port'])) for peer in raw_peers}

