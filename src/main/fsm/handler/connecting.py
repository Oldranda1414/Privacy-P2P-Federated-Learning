from typing import Callable, Awaitable
from asyncio import create_task

from peers import Peer

from fsm.state import State
from fsm.context import Context

CONNECTION_ATTEMPTS = 5

def get_connecting_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def connecting_handler() -> State:
        """Try connecting to all peers, with retries. Shutdown if any fail."""
        for peer in context.peers.values():
            if peer in context.comm.get_connected_peers():
                continue

            success = await _try_connect(peer, context)
            if not success:
                context.log.error(f"Unable to connect to {peer.node_id} after {CONNECTION_ATTEMPTS} attempts")
                return State.SHUTDOWN

        context.log.info("Successfully connected to all peers")
        _start_heartbeat_service(context)
        return State.SETUP
    return connecting_handler

async def _try_connect(peer: Peer, context: Context) -> bool:
    """Attempt to connect to a peer with retries."""
    for attempt in range(1, CONNECTION_ATTEMPTS + 1):
        if await context.comm.connect_to_peer(peer):
            context.log.info(f"Connected to {peer.node_id} (attempt {attempt})")
            return True
        context.log.warning(f"Attempt {attempt} to connect with {peer.node_id} failed")
    return False

def _start_heartbeat_service(context: Context):
    context.heartbeat_task = create_task(context.heartbeat_service.run())
