import asyncio

from fsm import FiniteStateMachine
from logger import get_logger

logger = get_logger("main", "main - %(levelname)s - %(message)s")

async def main():
    # Create fsm
    fsm = FiniteStateMachine()
    await fsm.run()

if __name__ == "__main__":
    asyncio.run(main())
    
