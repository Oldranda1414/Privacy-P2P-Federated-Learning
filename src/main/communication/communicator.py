import asyncio
from datetime import datetime
from typing import Awaitable, Callable, Dict

# TODO undestand this better to document it in report

from logger import get_logger
from peers import Peer
from communication.message import Message, MessageType


class AsyncCommunicator:
    def __init__(self, owner: Peer, quiet: bool = True):
        self.owner = owner
        self.server = None
        self.connections: Dict[Peer, asyncio.StreamWriter] = {}
        self.message_handlers: Dict[MessageType, Callable[[Peer, str, datetime], Awaitable[None]]] = {}
        self.running = False

        self.log = get_logger("com")
        self.log.disabled = quiet
        
    async def start_server(self):
        """Start the communication server"""
        self.server = await asyncio.start_server(
            self._handle_client, self.owner.host, self.owner.port
        )
        self.running = True
        self.log.info(f"Server started on {self.owner.host}:{self.owner.port}")
        
    async def stop_server(self):
        """Stop the communication server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            self.log.info("Server stopped")
            
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connections"""
        peer_addr = writer.get_extra_info('peername')
        self.log.info(f"New connection from {peer_addr}")
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = Message.decode(data)
                await self._process_message(message, writer)
                    
        except asyncio.CancelledError:
            self.log.error("CancelledError")
            pass
        except Exception as e:
            self.log.error(f"Error handling client {peer_addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            self.log.info(f"Connection closed for {peer_addr}")
            
    async def _process_message(self, message: Message, writer: asyncio.StreamWriter):
        """Process incoming messages"""
        
        self.log.info(f"Received {message.message_type} from {message.sender.node_id}: {message.content}")

        if message.message_type == MessageType.HANDSHAKE: # Handle handshake messages to register connections
            self.connections[message.sender] = writer
            response = Message(MessageType.HANDSHAKE_ACK, self.owner, message.sender, 'Connected successfully', datetime.now())
            await self._send_raw_message(writer, response)
        elif message.message_type in self.message_handlers.keys():
            await self.message_handlers[message.message_type](message.sender, message.content, message.timestamp)
        else:
            raise Exception(f"No handler registered for messege of type {message.message_type}")
                
    async def _send_raw_message(self, writer: asyncio.StreamWriter, message: Message):
        """Send raw message through a writer"""
        try:
            data = Message.encode(message)
            writer.write(data)
            await writer.drain()
        except Exception as e:
            self.log.error(f"Error sending message: {e}")
            
    async def connect_to_peer(self, peer: Peer):
        """Connect to a peer node"""
        try:
            reader, writer = await asyncio.open_connection(peer.host, peer.port)
            handshake = Message(MessageType.HANDSHAKE, self.owner, peer, f'Hello from {self.owner.node_id}', datetime.now())
            await self._send_raw_message(writer, handshake)
            
            # Wait for handshake acknowledgment
            response_data = await reader.readline()
            response = Message.decode(response_data)
            
            if response.message_type == MessageType.HANDSHAKE_ACK:
                self.connections[peer] = writer
                self.log.info(f"Successfully connected to {peer.node_id} at {peer.host}:{peer.port}")

                # Start listening for messages from this peer
                asyncio.create_task(self._listen_to_peer(reader, writer, peer))
                
        except Exception as e:
            self.log.error(f"Failed to connect to {peer.node_id} at {peer.host}:{peer.port}: {e}")
            
    async def _listen_to_peer(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, peer: Peer):
        """Listen for messages from a connected peer"""
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                    
                message = Message.decode(data)
                await self._process_message(message, writer)
                
        except Exception as e:
            self.log.error(f"Error listening to peer {peer.node_id}: {e}")
        finally:
            if peer in self.connections:
                del self.connections[peer]
                
    async def send_message(self, receiver: Peer, message_type: MessageType, content: str):
        """Send a message to a specific receiver"""
        if receiver not in self.connections:
            self.log.error(f"No connection to {receiver.node_id}")
            return False
        
        message = Message(message_type, self.owner, receiver, content, datetime.now())
        writer = self.connections[receiver]
        await self._send_raw_message(writer, message)
        self.log.info(f"Sent message to {receiver.node_id}: {content}")
        return True
        
    def register_message_handler(self, message_type: MessageType, handler: Callable):
        """Register a handler for incoming messages"""
        self.message_handlers[message_type] = handler
        
    async def broadcast_message(self, message_type: MessageType, content: str):
        """Broadcast a message to all connected peers"""
        tasks = []
        for receiver in self.connections:
            tasks.append(self.send_message(receiver, message_type, content))
        
        if tasks:
            await asyncio.gather(*tasks)
            self.log.info(f"Broadcasted message to {len(tasks)} peers: {content}")

    def get_connected_peers(self) -> set[Peer]:
        return set(self.connections.keys())

