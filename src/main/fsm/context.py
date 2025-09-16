from typing import TYPE_CHECKING
from asyncio import Task

from fsm.state import State
from fsm.handler.shutdown import get_stop
if TYPE_CHECKING: # Importing only for type checking to prevent circular import
    from fsm.handler.termination import TerminationVote

from machine_learning.model import Model
from machine_learning.dataset import Dataset
from machine_learning.history import History
from machine_learning.weights import Weights

from communication.communicator import AsyncCommunicator
from utils.logger import get_logger
from peers import Peer, load_self, load_peers
from heartbeat import HeartbeatService

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

        self.comm = AsyncCommunicator(self.owner, CONNECTION_TIMEOUT)
        self.heartbeat_service = HeartbeatService(self.comm, self.peers, get_stop(self), PULSE_INTERVAL, TIMEOUT)
        self.heartbeat_task: Task | None = None

        self.log = get_logger("context")
        self.log.disabled = quiet
        self.sync_peers: set[Peer] = set()

        self.model = Model()
        self.dataset: Dataset | None = None
        self.training_history: History | None = None
        self.received = ReceivedWeights()

        self.termination_votes: list[TerminationVote] = []
        self.rounds_done = 0

class ReceivedWeights:
    def __init__(self):
        self.partitions: list[Weights] = []
        self.subtotals: list[Weights] = []

    def reset(self):
        self.partitions: list[Weights] = []
        self.subtotals: list[Weights] = []

