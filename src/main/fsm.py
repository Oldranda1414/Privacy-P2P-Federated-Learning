import asyncio
from enum import Enum
from logging import shutdown
from typing import Callable, Awaitable

from logger import get_logger
from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer, load_peers, load_self
from heartbeat import HeartbeatService


PEER_JSON_FILE = "peers.json"
PULSE_INTERVAL = 10
TIMEOUT = 100

class State(Enum):
    SETUP = 1
    TRAINING = 2
    SECURE_AVARAGE_COMPUTATION = 3
    SHUTDOWN = 4
    IDLE = 5

class FiniteStateMachine:
    def __init__(self, quiet: bool = True):
        self.owner = load_self(PEER_JSON_FILE)
        self.peers = load_peers(PEER_JSON_FILE)
        self.state = State.SETUP
        self.handlers: dict[State, Callable[[], Awaitable[State]]] = {
                State.SETUP : self._setup_handler,
                State.SHUTDOWN : self._shutdown_handler,
                State.IDLE : self._idle_handler,
                # State.TRAINING : self._training_handler,
                # State.SECURE_AVARAGE_COMPUTATION : self._sac_handler
        }
        self.active = True

        self.comm = AsyncCommunicator(self.owner)
        self.heartbeat_service = HeartbeatService(self.comm, self.peers, self.stop, PULSE_INTERVAL, TIMEOUT)

        self.log = get_logger("fsm")
        self.log.disabled = quiet
        # self.done_peers: set[Peer] = set()  # track peers that reported "done"

        # Register network handler
        # self.comm.register_message_handler(MessageType.FSM, self._message_handler)

    async def run(self):
        """Main FSM loop"""
        await self.comm.start_server()
        self.heartbeat_task = asyncio.create_task(self.heartbeat_service.run())
        await asyncio.sleep(10)
        while self.active:
            await self._loop()

    async def stop(self):
        await self.comm.stop_server()
        self.heartbeat_task.cancel()
        try:
            await self.heartbeat_task
        except asyncio.CancelledError:
            self.log.info("terminated heartbeat service")
        self.active = False
        self.log.info(f"{self.owner} shutting down in state {self.state}")

    async def _loop(self):
            handler = self.handlers[self.state]
            self.state = await handler()

    async def _shutdown_handler(self) -> State:
        await self.stop()
        return State.SHUTDOWN

    async def _idle_handler(self) -> State:
        await asyncio.sleep(10)
        self.log.info("still idle")
        return State.IDLE

    async def _setup_handler(self) -> State:
        self.log.info("in setup")
        for peer in self.peers.values():
            if peer not in self.comm.get_connected_peers():
                self.log.info(f"attempting to connect to {peer.node_id}")
                await self.comm.connect_to_peer(peer)
                self.log.info(f"connected to {peer.node_id}!")
        self.log.info("connected to all peers")
        return State.IDLE

    # async def _message_handler(self, sender: Peer, content: str, _: str):
    #     if content == "done":
    #         self.log.info(f"Got DONE from {sender.node_id}")
    #         self.done_peers.add(sender)

