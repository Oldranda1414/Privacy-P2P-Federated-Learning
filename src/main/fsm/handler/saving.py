from typing import Callable, Awaitable
from asyncio import sleep

from fsm.state import State
from fsm.context import Context

def get_saving_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def saving_handler() -> State:
        # TODO save model here
        context.log.info("saving model")
        await sleep(3)
        return State.SHUTDOWN
    return saving_handler
