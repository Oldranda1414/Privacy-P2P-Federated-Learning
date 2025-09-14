import asyncio
from datetime import datetime, timedelta
from typing import Awaitable, Callable

from communication.communicator import AsyncCommunicator
from communication.message import MessageType
from peers import Peer
from utils.logger import get_logger

PULSE_CONTENT = "I'm alive!"

class HeartbeatService:
    def __init__(self, comm: AsyncCommunicator, peers: dict[str, Peer], shutdown_cb: Callable[[], Awaitable[None]], interval: float, timeout: float, quiet: bool = True):
        """
        :param comm: AsyncCommunicator
        :param peers: dict[str, Peer]
        :param shutdown_cb: callback to trigger node shutdown
        :param interval: how often to send heartbeat message to peers (seconds)
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

        self.log = get_logger("poll")
        self.log.disabled = quiet

        # Register handler for pong responses
        self.comm.register_message_handler(MessageType.HEARTBEAT, self._message_handler)

    async def run(self):
        """Main loop of polling service"""
        while self.active:
            start_time = datetime.now()
            self.log.info(f"starting new hearbeat at {start_time}")

            # Send pulse to all peers
            await self.comm.broadcast_message(MessageType.HEARTBEAT, PULSE_CONTENT)

            # Check timeouts
            now = datetime.now()
            
            dead_peers = []
            for peer, last in list(self.last_seen.items()):
                if now - last > timedelta(seconds=self.timeout):
                    dead_peers.append(peer)
                else:
                    self.log.info(f"[✓] {peer} alive (last seen {last})")
            
            # Handle dead peers after checking all
            if dead_peers:
                for peer in dead_peers:
                    self.log.info(f"[!] {peer} is considered DEAD → shutting down")
                await self.shutdown_cb()
                return

            # Calculate how long to sleep to maintain interval
            elapsed = (datetime.now() - start_time).total_seconds()
            sleep_time = max(0, self.interval - elapsed)
            
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    async def _message_handler(self, sender: Peer, content: str, _: datetime):
        if content == PULSE_CONTENT:
            self.log.info(f"received pulse from {sender}")
            self.last_seen[sender] = datetime.now()

