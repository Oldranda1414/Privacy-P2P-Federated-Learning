from asyncio import Task

from communication.communicator import AsyncCommunicator
from utils.logger import get_logger
from peers import Peer, load_self, load_peers
from heartbeat import HeartbeatService
from machine_learning.model import Model

from fsm.state import State
from fsm.handler.shutdown import get_stop

PEER_JSON_FILE = "peers.json"
PULSE_INTERVAL = 10
TIMEOUT = 100
CONNECTION_TIMEOUT = 10

class Context:
    def __init__(self, quiet: bool = True):
        self.owner = load_self(PEER_JSON_FILE)
        self.peers = load_peers(PEER_JSON_FILE)
        self.state = State.CONNECTING
        self.active = True
        self.rounds_done = 0

        self.model = Model()
        self.model_initialized = False

        self.comm = AsyncCommunicator(self.owner, CONNECTION_TIMEOUT)
        self.heartbeat_service = HeartbeatService(self.comm, self.peers, get_stop(self), PULSE_INTERVAL, TIMEOUT)
        self.heartbeat_task: Task | None = None

        self.log = get_logger("fsm")
        self.log.disabled = quiet
        self.sync_peers: set[Peer] = set()  # track peers that reported "done"

