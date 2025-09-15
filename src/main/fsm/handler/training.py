from typing import Callable, Awaitable
from asyncio import sleep

from fsm.state import State
from fsm.context import Context

def get_training_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def training_handler() -> State:
        if context.dataset:
            context.log.info(f"training...")
            try: 
                context.model.train(context.dataset)
            except Exception as e:
                context.log.error(f"error occurred during training step: {e}")
                raise e
        else:
            context.log.error("Dataset not loaded, unable to train")
        return State.WAITING_FOR_PEERS
    return training_handler
