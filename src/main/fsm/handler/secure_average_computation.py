from typing import Callable, Awaitable
from asyncio import sleep
from datetime import datetime
from logging import Logger

from communication.message import MessageType
from communication.encodable import Encodable
from communication.communicator import AsyncCommunicator

from fsm.state import State
from fsm.context import Context

from sac import generate_partitions
from peers import Peer
from machine_learning.weights import Weights, sum_weights

def get_sac_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.PARTITIONED_WEIGHTS, _get_partition_message_handler(context))
    context.comm.register_message_handler(MessageType.SUBTOTAL_WEIGHTS, _get_subtotal_message_handler(context))
    async def secure_average_computation_handler() -> State:
        peers = list(context.peers.values())
        number_of_peers = len(peers)
        number_of_partitions = number_of_peers + 1
        sleep_time = 5
        context.log.info("doing sac...")

        weight_partitions = generate_partitions(context.model.get_weights(), number_of_partitions)
        kept_partition = weight_partitions[0]
        await _send_weights(context.comm, peers, weight_partitions[1:])
        await _wait_for_sync(context.received_weights, number_of_peers, context.log, sleep_time, "PARTITION")

        calculated_subtotal = sum_weights([kept_partition] + context.received_weights)
        await context.comm.broadcast_message(MessageType.SUBTOTAL_WEIGHTS, calculated_subtotal)
        await _wait_for_sync(context.received_subtotals, number_of_peers, context.log, sleep_time, "SUBTOTAL")
        new_weights = sum_weights([calculated_subtotal] + context.received_subtotals)
        context.model.set_weights(new_weights)

        # reset context arrays for new iteration
        context.received_weights = []
        context.received_subtotals = []

        if _training_complete(context):
            return State.SAVING_MODEL
        return State.TRAINING
    return secure_average_computation_handler

def _get_partition_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.received_weights.append(content)
            context.log.info("received partitioned weights")
        else:
            raise ValueError("partitioned weights received are not compatible")
    return message_handler

def _get_subtotal_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.received_subtotals.append(content)
            context.log.info("received subtotal weights")
        else:
            raise ValueError("subtotal weights received are not compatible")
    return message_handler

async def _wait_for_sync(to_be_filled: list, filled_len: int, log: Logger, sleep_time: int, name: str):
    while len(to_be_filled) < filled_len:
        log.info(f"{name} - waiting for {filled_len - len(to_be_filled)} peers")
        await sleep(sleep_time)

async def _send_weights(comm: AsyncCommunicator, peers: list[Peer], weights: list[Weights]):
    if len(peers) != len(weights):
        raise ValueError("peers and weights length must be the same")
    for i in range(len(peers)):
        await comm.send_message(peers[i], MessageType.PARTITIONED_WEIGHTS, weights[i])

def _training_complete(context: Context) -> bool:
    context.rounds_done += 1
    if context.rounds_done == 4:
        return True
    return False

