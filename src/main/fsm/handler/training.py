from typing import Callable, Awaitable
from random import uniform
from asyncio import sleep

from fsm.state import State
from fsm.context import Context

def get_training_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def training_handler() -> State:
        # TODO do actual training here
        train_time = int(uniform(3,10))
        context.log.info(f"training for {train_time}")
        await sleep(train_time)
        return State.WAITING_FOR_PEERS
    return training_handler
