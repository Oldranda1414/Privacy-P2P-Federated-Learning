from asyncio import create_task, sleep
from typing import Callable, Awaitable
from datetime import datetime

from fsm.state import State
from fsm.context import Context

from communication.message import MessageType
from machine_learning.weights import Weights
from communication.encodable import Encodable
from peers import Peer

def get_setup_handler(context: Context) -> Callable[[], Awaitable[State]]:
    # TODO change weights to initial weight in message type
    context.comm.register_message_handler(MessageType.WEIGHTS, _get_message_handler(context))
    async def setup_handler() -> State:
        if context.owner.node_id == "node1":
            initial_weights = context.model.get_weights() 
            await context.comm.broadcast_message(MessageType.WEIGHTS, initial_weights)
            context.model_initialized = True
        else:
            while not context.model_initialized:
                await sleep(5)
        context.heartbeat_task = create_task(context.heartbeat_service.run())
        return State.TRAINING
    return setup_handler

def _get_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.model.set_weights(content)
            context.model_initialized = True
            context.log.info("received initial weights")
        else:
            raise ValueError("initial weights received are not compatible")
    return message_handler


