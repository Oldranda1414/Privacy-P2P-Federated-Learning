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

class FiniteStateMachine:
    def __init__(self, quiet: bool = True):
        self.context = Context(quiet)
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
        self.context.state = await handler()
