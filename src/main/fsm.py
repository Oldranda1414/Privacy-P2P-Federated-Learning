import asyncio
import random

from logger import get_logger
from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer

logger = get_logger("fsm", "fsm - %(levelname)s - %(message)s")

class FiniteStateMachine:
    def __init__(self, comm: AsyncCommunicator, peers: dict[str, Peer], rounds: int):
        self.comm = comm
        self.peers = peers
        self.state = "working"
        self.handlers = {
            "working": self._working_handler,
            "waiting": self._waiting_handler,
        }
        self.active = True
        self.done_peers: set[Peer] = set()  # track peers that reported "done"
        self.rounds = rounds
        self.current_round = 1

        # Register network handler
        self.comm.register_message_handler(MessageType.FSM, self._message_handler)

    async def run(self):
        """Main FSM loop"""
        while self.active:
            handler = self.handlers[self.state]
            self.state = await handler()

    async def shutdown(self):
        self.active = False

    async def _working_handler(self) -> str:
        # Do some fake work
        duration = random.randint(3, 10)
        logger.info(f"Working for {duration} seconds...")
        await asyncio.sleep(duration)
        logger.info(f"finished working")

        # After work, tell peers you're done
        for peer in self.peers.values():
            await self.comm.send_message(peer, MessageType.FSM, "done")
        self.done_peers = set()  # reset
        return "waiting"

    async def _waiting_handler(self) -> str:
        logger.info(f"Waiting for peers to finish...")
        # Wait until all peers are done
        while set(self.peers.values()) - self.done_peers:
            await asyncio.sleep(3)
        if self.current_round < self.rounds:
            self.current_round += 1
            logger.info(f" All peers finished, starting round {self.current_round}")
        else:
            logger.info(f" All peers finished, all rounds finished, shutting down")
            await self.shutdown()
        
        return "working"

    async def _message_handler(self, sender: Peer, content: str, _: str):
        if content == "done":
            logger.info(f"Got DONE from {sender.node_id}")
            self.done_peers.add(sender)

