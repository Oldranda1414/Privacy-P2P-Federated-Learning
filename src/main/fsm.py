import asyncio
from enum import Enum
from logging import shutdown
from typing import Callable, Awaitable

from logger import get_logger
from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer, load_peers, load_self
from polling import PollingService

logger = get_logger("fsm", "fsm - %(levelname)s - %(message)s")

PEER_JSON_FILE = "peers.json"
INTERVAL = 2
TIMEOUT = 10

class State(Enum):
    SETUP = 1
    TRAINING = 2
    SECURE_AVARAGE_COMPUTATION = 3
    SHUTDOWN = 4

class FiniteStateMachine:
    def __init__(self):
        self.owner = load_self(PEER_JSON_FILE)
        self.peers = load_peers(PEER_JSON_FILE)
        self.comm = AsyncCommunicator(self.owner, False)
        self.state = State.SETUP
        self.handlers: dict[State, Callable[[], Awaitable[State]]] = {
                State.SETUP : self._setup_handler,
                State.SHUTDOWN : self._shutdown_handler,
                # State.TRAINING : self._training_handler,
                # State.SECURE_AVARAGE_COMPUTATION : self._sac_handler
        }
        self.active = True
        # self.done_peers: set[Peer] = set()  # track peers that reported "done"

        # Register network handler
        # self.comm.register_message_handler(MessageType.FSM, self._message_handler)

    async def run(self):
        """Main FSM loop"""
        await self.comm.start_server()
        poller = PollingService(self.comm, self.peers, self.stop, INTERVAL, TIMEOUT, True)
        asyncio.create_task(poller.run())
        await asyncio.sleep(10)
        while self.active:
            await self._loop()


    async def stop(self):
        await self.comm.stop_server()
        self.active = False
        logger.info(f"Node {self.owner} shutting down")
        # asyncio.get_event_loop().stop()

    async def _loop(self):
            handler = self.handlers[self.state]
            self.state = await handler()

    async def _shutdown_handler(self) -> State:
        await self.stop()
        return State.SHUTDOWN

    async def _setup_handler(self) -> State:
        logger.info("in setup")
        for peer in self.peers.values():
            if peer not in self.comm.get_connected_peers():
                logger.info(f"attempting to connect to {peer.node_id}")
                await self.comm.connect_to_peer(peer)
                logger.info(f"connected to {peer.node_id}!")
        logger.info("connected to all peers, shutting down")
        return State.SHUTDOWN

    # async def _message_handler(self, sender: Peer, content: str, _: str):
    #     if content == "done":
    #         logger.info(f"Got DONE from {sender.node_id}")
    #         self.done_peers.add(sender)

