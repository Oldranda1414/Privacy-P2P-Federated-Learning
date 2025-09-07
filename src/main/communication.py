import asyncio
import json
import logging
from typing import Awaitable, Callable, Dict, Any
from datetime import datetime

# TODO undestand this better to document it in report

from peers import Peer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncCommunicator:
    def __init__(self, peer: Peer, verbose: bool):
        self.host = peer.host
        self.port = peer.port
        self.node_id = peer.node_id
        logger.disabled = not verbose
        self.server = None
        self.connections: Dict[str, asyncio.StreamWriter] = {}
        self.message_handlers: Dict[str, Callable[[str, str, str], Awaitable[None]]] = {}
        self.running = False
        
    async def start_server(self):
        """Start the communication server"""
        self.server = await asyncio.start_server(
            self._handle_client, self.host, self.port
        )
        self.running = True
        logger.info(f"Server started on {self.host}:{self.port}")
        
    async def stop_server(self):
        """Stop the communication server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            logger.info("Server stopped")
            
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connections"""
        peer_addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {peer_addr}")
        
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                    
                try:
                    message = json.loads(data.decode().strip())
                    await self._process_message(message, writer)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received from {peer_addr}")
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error handling client {peer_addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Connection closed for {peer_addr}")
            
    async def _process_message(self, message: Dict[str, Any], writer: asyncio.StreamWriter):
        """Process incoming messages"""
        msg_type = message.get('type')
        sender = str(message.get('sender'))
        content = str(message.get('content'))
        timestamp = str(message.get('timestamp'))
        
        logger.info(f"Received {msg_type} from {sender}: {content}")
        
        # Handle handshake messages to register connections
        if msg_type == 'handshake':
            self.connections[sender] = writer
            response = {
                'type': 'handshake_ack',
                'sender': self.node_id,
                'receiver': sender,
                'content': 'Connected successfully',
                'timestamp': datetime.now().isoformat()
            }
            await self._send_raw_message(writer, response)
            
        # Handle regular messages
        elif msg_type == 'message':
            if 'message' in self.message_handlers:
                await self.message_handlers['message'](sender, content, timestamp)
                
    async def _send_raw_message(self, writer: asyncio.StreamWriter, message: Dict[str, Any]):
        """Send raw message through a writer"""
        try:
            data = json.dumps(message) + '\n'
            writer.write(data.encode())
            await writer.drain()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    async def connect_to_peer(self, peer: Peer):
        """Connect to a peer node"""
        try:
            reader, writer = await asyncio.open_connection(peer.host, peer.port)
            
            # Send handshake
            handshake = {
                'type': 'handshake',
                'sender': self.node_id,
                'receiver': peer.node_id,
                'content': f'Hello from {self.node_id}',
                'timestamp': datetime.now().isoformat()
            }
            
            await self._send_raw_message(writer, handshake)
            
            # Wait for handshake acknowledgment
            response_data = await reader.readline()
            response = json.loads(response_data.decode().strip())
            
            if response.get('type') == 'handshake_ack':
                self.connections[peer.node_id] = writer
                logger.info(f"Successfully connected to {peer.node_id} at {peer.host}:{peer.port}")
                
                # Start listening for messages from this peer
                asyncio.create_task(self._listen_to_peer(reader, writer, peer.node_id))
                
        except Exception as e:
            logger.error(f"Failed to connect to {peer.node_id} at {peer.host}:{peer.port}: {e}")
            
    async def _listen_to_peer(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, peer_id: str):
        """Listen for messages from a connected peer"""
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                    
                message = json.loads(data.decode().strip())
                await self._process_message(message, writer)
                
        except Exception as e:
            logger.error(f"Error listening to peer {peer_id}: {e}")
        finally:
            if peer_id in self.connections:
                del self.connections[peer_id]
                
    async def send_message(self, receiver: str, content: str):
        """Send a message to a specific receiver"""
        if receiver not in self.connections:
            logger.error(f"No connection to {receiver}")
            return False
            
        message = {
            'type': 'message',
            'sender': self.node_id,
            'receiver': receiver,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        writer = self.connections[receiver]
        await self._send_raw_message(writer, message)
        logger.info(f"Sent message to {receiver}: {content}")
        return True
        
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for incoming messages"""
        self.message_handlers[message_type] = handler
        
    async def broadcast_message(self, content: str):
        """Broadcast a message to all connected peers"""
        tasks = []
        for receiver in self.connections.keys():
            tasks.append(self.send_message(receiver, content))
        
        if tasks:
            await asyncio.gather(*tasks)
            logger.info(f"Broadcasted message to {len(tasks)} peers: {content}")

