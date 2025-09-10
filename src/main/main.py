import asyncio

from fsm import FiniteStateMachine
from logger import get_logger
from environment import get_self_id


async def main():
    log = get_logger("main")

    # Create fsm
    fsm = FiniteStateMachine((not get_self_id() == "node1"))
    fsm_task = asyncio.create_task(fsm.run())

    try:
        # Wait for FSM to complete or handle interrupts
        await fsm_task
    except KeyboardInterrupt:
        log.info("Received interrupt signal")
        await fsm.stop()
        await fsm_task
    except Exception as e:
        log.error(f"FSM encountered error: {e}")
    finally:
        log.info("Program terminated")

if __name__ == "__main__":
    asyncio.run(main())
    
