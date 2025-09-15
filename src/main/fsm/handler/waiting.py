from asyncio import sleep
from logging import Logger
from typing import Sized

WAIT_TIME = 5

async def wait_for_sync(collection: Sized, filled_len: int, log: Logger, name: str):
    while len(collection) < filled_len:
        log.info(f"{name} - waiting for {filled_len - len(collection)} peers")
        await sleep(WAIT_TIME)
