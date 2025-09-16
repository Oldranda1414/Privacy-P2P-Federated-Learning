from typing import Callable, Awaitable

from fsm.state import State
from fsm.context import Context

SAVE_PATH = "output/model.keras"

def get_saving_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def saving_handler() -> State:
        context.model.save(SAVE_PATH)
        context.log.info(f"training completed in {context.rounds_done} rounds")
        return State.SHUTDOWN
    return saving_handler
