import asyncio

from peers import load_self, load_peers
from communication.communicator import AsyncCommunicator
from polling import PollingService
from fsm import FSM

from output import fprint

INTERVAL = 10
TIMEOUT = 60

async def main():
    global comm
    self = load_self()
    peers = load_peers()

    comm = AsyncCommunicator(self, False)
    await comm.start_server()

    # Connect to peers
    for peer in peers.values():
        await comm.connect_to_peer(peer)

    # Create FSM
    fsm = FSM(comm, peers, 3)

    # Shutdown callback
    async def shutdown():
        await comm.stop_server()
        fprint(f"Node {self.node_id} shutting down due to peer failure")
        asyncio.get_event_loop().stop()

    # Create poller
    poller = PollingService(comm, peers, shutdown, INTERVAL, TIMEOUT, False)

    asyncio.create_task(fsm.run())
    asyncio.create_task(poller.run())
    print("finished setup, running indefenetly")

    try:
        await asyncio.Future()  # keep running until stopped
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())

