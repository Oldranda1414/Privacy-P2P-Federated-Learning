from typing import Callable, Awaitable
from asyncio import sleep

from fsm.state import State
from fsm.context import Context

def get_training_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def training_handler() -> State:
        if context.dataset:
            context.log.info(f"training...")
            await sleep(5)
            # context.model.train(context.dataset)
        else:
            context.log.error("Dataset not loaded, unable to train")
        return State.WAITING_FOR_PEERS
    return training_handler
