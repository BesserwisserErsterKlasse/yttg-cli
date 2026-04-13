# flake8: noqa: E402
# isort: skip_file
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())  # Python3.14 behavior fix

from asyncio import run
from typing import NoReturn

from globalobjects import cli, client


async def main() -> NoReturn:
    await client.start()
    await cli.start()


if __name__ == '__main__':
    run(main())
