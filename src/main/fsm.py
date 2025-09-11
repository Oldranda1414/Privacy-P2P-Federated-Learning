import asyncio
from random import uniform
from enum import Enum
from typing import Callable, Awaitable
from datetime import datetime

from logger import get_logger
from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer, load_peers, load_self
from heartbeat import HeartbeatService


PEER_JSON_FILE = "peers.json"
PULSE_INTERVAL = 10
TIMEOUT = 100

class State(Enum):
    CONNECTING = 1
    SETUP = 2
    TRAINING = 3
    WAITING_FOR_PEERS = 4
    SECURE_AVARAGE_COMPUTATION = 5
    SAVING_MODEL = 6
    SHUTDOWN = 7

class FiniteStateMachine:
    def __init__(self, quiet: bool = True):
        self.owner = load_self(PEER_JSON_FILE)
        self.peers = load_peers(PEER_JSON_FILE)
        self.state = State.CONNECTING
        self.handlers: dict[State, Callable[[], Awaitable[State]]] = {
                State.CONNECTING : self._connecting_handler,
                State.SETUP : self._setup_handler,
                State.TRAINING : self._training_handler,
                State.WAITING_FOR_PEERS : self._waiting_handler,
                State.SECURE_AVARAGE_COMPUTATION : self._sac_handler,
                State.SAVING_MODEL : self._saving_handler,
                State.SHUTDOWN : self._shutdown_handler
        }
        self.active = True

        self.rounds_done = 0

        self.comm = AsyncCommunicator(self.owner)
        self.heartbeat_service = HeartbeatService(self.comm, self.peers, self.stop, PULSE_INTERVAL, TIMEOUT)
        self.heartbeat_task: asyncio.Task | None = None

        self.log = get_logger("fsm")
        self.log.disabled = quiet
        self.sync_peers: set[Peer] = set()  # track peers that reported "done"

        # Register network handler
        self.comm.register_message_handler(MessageType.SYNC, self._sync_handler)

    async def run(self):
        """Main FSM loop"""
        await self.comm.start_server()
        await asyncio.sleep(10)
        while self.active:
            await self._loop()

    async def stop(self):
        await self.comm.stop_server()
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                self.log.info("terminated heartbeat service")
        self.active = False
        self.log.info(f"{self.owner} shutting down in {self.state}")

    async def _loop(self):
            handler = self.handlers[self.state]
            self.state = await handler()

    async def _connecting_handler(self) -> State:
        # TODO have a max number of attempts and then shutdown
        for peer in self.peers.values():
            if peer not in self.comm.get_connected_peers():
                self.log.info(f"attempting to connect to {peer.node_id}")
                await self.comm.connect_to_peer(peer)
                self.log.info(f"connected to {peer.node_id}!")
        self.log.info("connected to all peers")
        return State.SETUP

    async def _setup_handler(self) -> State:
        # TODO add receival of starting weights
        self.heartbeat_task = asyncio.create_task(self.heartbeat_service.run())
        return State.TRAINING

    async def _training_handler(self) -> State:
        # TODO do actual training here
        train_time = int(uniform(3,10))
        self.log.info(f"training for {train_time}")
        await asyncio.sleep(train_time)
        return State.WAITING_FOR_PEERS

    async def _waiting_handler(self) -> State:
        await self.comm.broadcast_message(MessageType.SYNC, "I am done!")
        while len(self.sync_peers) < len(self.peers):
            self.log.info("waiting for {len(self.peers) - len(self.sync_peers)} peers to be ready")
            await asyncio.sleep(5)

        return State.SECURE_AVARAGE_COMPUTATION

    async def _sac_handler(self) -> State:
        # TODO do actual SAC here
        sac_time = 10
        self.log.info(f"doing sac for {sac_time}")
        await asyncio.sleep(sac_time)
        if self._training_complete():
            return State.SAVING_MODEL
        return State.TRAINING

    async def _saving_handler(self) -> State:
        # TODO save model here
        self.log.info("saving model")
        await asyncio.sleep(3)
        return State.SHUTDOWN

    async def _shutdown_handler(self) -> State:
        await self.stop()
        return State.SHUTDOWN

    def _training_complete(self) -> bool:
        self.rounds_done += 1
        if self.rounds_done == 5:
            return True
        return False

    async def _sync_handler(self, sender: Peer, _content: str, _timestamp: datetime):
        self.log.info(f"Got SYNC from {sender}")
        self.sync_peers.add(sender)

