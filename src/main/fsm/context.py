from asyncio import Task
from typing import Optional

from communication.communicator import AsyncCommunicator
from machine_learning.weights import Weights
from utils.logger import get_logger
from peers import Peer, load_self, load_peers
from heartbeat import HeartbeatService
from machine_learning.model import Model
from machine_learning.dataset import Dataset

from fsm.state import State
from fsm.handler.shutdown import get_stop

PULSE_INTERVAL = 10
TIMEOUT = 100
CONNECTION_TIMEOUT = 10

class Context:
    def __init__(self, quiet: bool = True):
        self.owner = load_self()
        # TODO check if peers are ever used as dictionary or if they are always turned to list
        self.peers = load_peers()
        self.state = State.CONNECTING
        self.active = True
        self.rounds_done = 0

        self.model = Model()
        self.dataset: Optional[Dataset] = None
        # TODO consider creating custom data object for this stuff
        self.received_weights: list[Weights] = []
        self.received_subtotals: list[Weights] = []

        self.comm = AsyncCommunicator(self.owner, CONNECTION_TIMEOUT)
        self.heartbeat_service = HeartbeatService(self.comm, self.peers, get_stop(self), PULSE_INTERVAL, TIMEOUT)
        self.heartbeat_task: Task | None = None

        self.log = get_logger("fsm")
        self.log.disabled = quiet
        self.sync_peers: set[Peer] = set()  # track peers that reported "done"

