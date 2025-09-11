from asyncio import create_task
from typing import Callable, Awaitable

from fsm.state import State
from fsm.context import Context

def get_setup_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def setup_handler() -> State:
        # TODO add receival of starting weights
        context.heartbeat_task = create_task(context.heartbeat_service.run())
        return State.TRAINING

    return setup_handler
