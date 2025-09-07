import json
import os

from environment import get_self_id
from output import fprint

class Peer:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port

def load_self(peers_file: str = "./peers.json") -> Peer:
    self_id = get_self_id()
    peers = _load_peer_file(peers_file)
    return peers.pop(self_id)

def load_peers(peers_file: str = "peers.json") -> dict[str, Peer]:
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
    fprint(f"Loaded {len(raw_peers)})")
    return {peer['node_id']: Peer(peer['node_id'], peer['host'], int(peer['port'])) for peer in raw_peers}

