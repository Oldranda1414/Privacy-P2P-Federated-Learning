from typing import Callable, Awaitable
from asyncio import sleep

from fsm.state import State
from fsm.context import Context

def get_sac_handler(context: Context) -> Callable[[], Awaitable[State]]:
    async def secure_average_computation_handler() -> State:
        # TODO do actual SAC here
        sac_time = 3
        context.log.info(f"doing sac for {sac_time}")
        await sleep(sac_time)
        if _training_complete(context):
            return State.SAVING_MODEL
        return State.TRAINING
    return secure_average_computation_handler

def _training_complete(context: Context) -> bool:
    context.rounds_done += 1
    if context.rounds_done == 4:
        return True
    return False
