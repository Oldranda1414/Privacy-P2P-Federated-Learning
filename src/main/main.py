import asyncio

from peers import load_self, load_peers
from communication.communicator import AsyncCommunicator
from polling import PollingService
from fsm import FiniteStateMachine

from logger import get_logger

logger = get_logger("main", "main - %(levelname)s - %(message)s")

INTERVAL = 10
TIMEOUT = 60
PEER_JSON_FILE = "peers.json"

async def main():
    global comm
    self = load_self(PEER_JSON_FILE)
    peers = load_peers(PEER_JSON_FILE)

    comm = AsyncCommunicator(self, False)
    await comm.start_server()

    # Connect to peers
    for peer in peers.values():
        await comm.connect_to_peer(peer)

    # Create fsm
    fsm = FiniteStateMachine(comm, peers, 3)

    # Shutdown callback
    async def shutdown():
        await comm.stop_server()
        logger.info(f"Node {self.node_id} shutting down due to peer failure")
        asyncio.get_event_loop().stop()

    # Create poller
    poller = PollingService(comm, peers, shutdown, INTERVAL, TIMEOUT, False)

    asyncio.create_task(fsm.run())
    asyncio.create_task(poller.run())
    logger.info("finished setup, running indefenetly")

    try:
        await asyncio.Future()  # keep running until stopped
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())

