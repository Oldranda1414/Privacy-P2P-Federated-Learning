from typing import Callable, Awaitable
from asyncio import sleep

from fsm.state import State
from fsm.context import Context
from fsm.handler.connecting import get_connecting_handler
from fsm.handler.setup import get_setup_handler
from fsm.handler.training import get_training_handler
from fsm.handler.waiting import get_waiting_handler
from fsm.handler.secure_average_computation import get_sac_handler
from fsm.handler.saving import get_saving_handler
from fsm.handler.shutdown import get_shutdown_handler
from utils.logger import get_logger

class FiniteStateMachine:
    def __init__(self, quiet: bool = True, handler_quiet: bool = True):
        self.log = get_logger("fsm")
        self.log.disabled = quiet
        self.context = Context(handler_quiet)
        self.handlers: dict[State, Callable[[], Awaitable[State]]] = {
            State.CONNECTING : get_connecting_handler(self.context),
            State.SETUP : get_setup_handler(self.context),
            State.TRAINING : get_training_handler(self.context),
            State.WAITING_FOR_PEERS : get_waiting_handler(self.context),
            State.SECURE_AVERAGE_COMPUTATION : get_sac_handler(self.context),
            State.SAVING_MODEL : get_saving_handler(self.context),
            State.SHUTDOWN : get_shutdown_handler(self.context)
        }

    async def run(self):
        """Main FSM loop"""
        await self.context.comm.start_server()
        await sleep(10)
        while self.context.active:
            await self._loop()

    async def _loop(self):
        handler = self.handlers[self.context.state]
        new_state = await handler()
        if new_state != self.context.state:
            self.log.info(f"Transitioning to {new_state.value} state")
            self.context.state = new_state
