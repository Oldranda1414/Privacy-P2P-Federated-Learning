from typing import Callable, Awaitable
from datetime import datetime

from communication.message import MessageType
from communication.encodable import Encodable
from communication.communicator import AsyncCommunicator

from fsm.state import State
from fsm.context import Context
from fsm.handler.waiting import wait_for_sync

from sac import generate_partitions
from peers import Peer
from machine_learning.weights import Weights, sum_weights

# TODO check if this is a good value
ACCURACY_THRESHOLD = 0.88
MAX_ROUNDS = 9

def get_sac_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.PARTITIONED_WEIGHTS, _get_partition_message_handler(context))
    context.comm.register_message_handler(MessageType.SUBTOTAL_WEIGHTS, _get_subtotal_message_handler(context))
    async def secure_average_computation_handler() -> State:
        peers = list(context.peers.values())
        number_of_peers = len(peers)
        number_of_partitions = number_of_peers + 1
        context.log.info("doing sac...")

        weight_partitions = generate_partitions(context.model.get_weights(), number_of_partitions)
        kept_partition = weight_partitions[0]
        await _send_weights(context.comm, peers, weight_partitions[1:])
        await wait_for_sync(context.received.partitions, number_of_peers, context.log, "PARTITION")

        calculated_subtotal = sum_weights([kept_partition] + context.received.partitions)
        await context.comm.broadcast_message(MessageType.SUBTOTAL_WEIGHTS, calculated_subtotal)
        await wait_for_sync(context.received.subtotals, number_of_peers, context.log, "SUBTOTAL")
        new_weights = sum_weights([calculated_subtotal] + context.received.subtotals) / number_of_partitions
        context.model.set_weights(new_weights)

        # reset context arrays for new iteration
        context.received.reset()

        if _training_complete(context):
            return State.SAVING_MODEL
        return State.TRAINING
    return secure_average_computation_handler

def _get_partition_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.received.partitions.append(content)
            context.log.info("received partitioned weights")
        else:
            raise ValueError("partitioned weights received are not compatible")
    return message_handler

def _get_subtotal_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.received.subtotals.append(content)
            context.log.info("received subtotal weights")
        else:
            raise ValueError("subtotal weights received are not compatible")
    return message_handler

async def _send_weights(comm: AsyncCommunicator, peers: list[Peer], weights: list[Weights]):
    if len(peers) != len(weights):
        raise ValueError("peers and weights length must be the same")
    for i in range(len(peers)):
        await comm.send_message(peers[i], MessageType.PARTITIONED_WEIGHTS, weights[i])

# TODO ensure all hosts are okey with stopping here.
def _training_complete(context: Context) -> bool:
    if context.training_history:
        context.rounds_done += 1
        current_accuracy = context.training_history.validation_accuracy[-1]
        context.log.info(f"accuracy obtained: {current_accuracy}")
        if current_accuracy >= ACCURACY_THRESHOLD:
            return True
        elif context.rounds_done >= MAX_ROUNDS:
            return True

    return False

