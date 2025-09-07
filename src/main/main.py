import asyncio
from communication import AsyncCommunicator

from peers import load_peers, load_self
from output import fprint

comm: AsyncCommunicator | None = None
RUN_TIMEOUT = 5

async def example_message_handler(sender: str, content: str, timestamp: str):
    """Example message handler"""
    print(f"[{timestamp}] message from {sender}: {content}")
    if comm:
        if content == "ping":
            await comm.send_message(sender, "pong")
        if content == "pong":
            await comm.send_message(sender, "ping")

async def main():

    global comm

    try:
        self = load_self()
        peers = load_peers()
    except Exception as e:
        fprint(f"Error loading peers: {e}")
        fprint(f"Shutting down...")
        return

    fprint(f"Starting {self.node_id}")
    comm = AsyncCommunicator(self, False)
    
    # Register message handler
    comm.register_message_handler('message', example_message_handler)
    
    # Start server
    await comm.start_server()

    # Add a small delay to ensure all peers are ready
    await asyncio.sleep(10)

    # Connect to other peers
    for peer in peers.values():
        fprint(f"Attempting to connect to {peer.node_id} at {peer.host}:{peer.port}")
        await comm.connect_to_peer(peer)
        await asyncio.sleep(1)  # Give connection time to establish

    if self.node_id == "node1":
        for peer in peers.values():
            await comm.send_message(peer.node_id, "ping")

    try:
        await asyncio.wait_for(asyncio.Future(), timeout=RUN_TIMEOUT)
    except asyncio.TimeoutError:
        fprint("Timeout reached, shutting down...")
    finally:
        await comm.stop_server()
        fprint(f"Ending {self.node_id}")

if __name__ == "__main__":
    asyncio.run(main())

