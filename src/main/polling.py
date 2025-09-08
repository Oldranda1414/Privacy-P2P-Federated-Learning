import asyncio
from datetime import datetime, timedelta
from typing import Awaitable, Callable

from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer
from logger import get_logger

logger = get_logger("poll", "poll - %(levelname)s - %(message)s")

# TODO change polling to heartbeat if deemed better

class PollingService:
    def __init__(self, comm: AsyncCommunicator, peers: dict[str, Peer], shutdown_cb: Callable[[], Awaitable[None]], interval: float, timeout: float, verbose:bool = False):
        """
        :param comm: AsyncCommunicator
        :param peers: dict[node_id, Peer]
        :param shutdown_cb: callback to trigger node shutdown
        :param interval: how often to ping peers (seconds)
        :param timeout: how long until a peer is considered dead
        """
        self.comm = comm
        self.peers = peers
        self.interval = interval
        self.timeout = timeout
        self.shutdown_cb = shutdown_cb
        self.last_seen: dict[Peer, datetime] = {
            peer: datetime.now() for peer in peers.values()
        }
        self.active = True
        logger.disabled = not verbose

        # Register handler for pong responses
        self.comm.register_message_handler(MessageType.POLLING, self._message_handler)

    async def run(self):
        """Main loop of polling service"""
        while self.active:
            # Send ping to all peers
            for peer_id in self.peers.keys():
                await self.comm.send_message(self.peers[peer_id], MessageType.POLLING, "ping")

            # Check timeouts
            now = datetime.now()
            for peer, last in list(self.last_seen.items()):
                if now - last > timedelta(seconds=self.timeout):
                    logger.info(f"[!] Peer {peer.node_id} is considered DEAD → shutting down")
                    await self.shutdown_cb()
                    return
                else:
                    logger.info(f"[✓] Peer {peer.node_id} alive (last seen {last})")

            await asyncio.sleep(self.interval)

    async def _message_handler(self, sender: Peer, content: str, _: datetime):
        if content == "ping":
            await self.comm.send_message(sender, MessageType.POLLING, "pong")
        elif content == "pong":
            self.last_seen[sender] = datetime.now()

