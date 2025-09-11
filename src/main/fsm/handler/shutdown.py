from typing import Callable, Awaitable, TYPE_CHECKING
from asyncio import CancelledError

from fsm.state import State
if TYPE_CHECKING: # Importing only for type checking to prevent circular import
    from fsm.context import Context

def get_shutdown_handler(context: 'Context') -> Callable[[], Awaitable[State]]:
    async def shutdown_handler() -> State:
        await get_stop(context)()
        return State.SHUTDOWN
    return shutdown_handler 

def get_stop(context: 'Context') -> Callable[[], Awaitable[None]]:
    async def stop():
        await context.comm.stop_server()
        if context.heartbeat_task:
            context.heartbeat_task.cancel()
            try:
                await context.heartbeat_task
            except CancelledError:
                context.log.info("terminated heartbeat service")
        context.active = False
        context.log.info(f"{context.owner} shutting down in {context.state}")
    return stop
