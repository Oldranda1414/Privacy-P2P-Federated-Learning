from asyncio import create_task, run

from fsm.finite_state_machine import FiniteStateMachine
from fsm.handler.shutdown import get_stop
from utils.logger import get_logger
from environment import get_self_id


async def main():
    log = get_logger("main")

    # Create fsm
    fsm = FiniteStateMachine((not get_self_id() == "node2"))
    fsm_task = create_task(fsm.run())

    try:
        # Wait for FSM to complete or handle interrupts
        await fsm_task
    except KeyboardInterrupt:
        log.info("Received interrupt signal")
        await get_stop(fsm.context)()
        await fsm_task
    except Exception as e:
        log.error(f"FSM encountered error: {e}")
    finally:
        log.info("Program terminated")

if __name__ == "__main__":
    run(main())
    
