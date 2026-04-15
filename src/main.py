# flake8: noqa: E402
# isort: skip_file
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())  # Python3.14 behavior fix

from asyncio import run
from typing import NoReturn

from client.types import DownloadProgressResponse
from globalobjects import cli, client, progress_bar


@client.on_background_response(DownloadProgressResponse)
async def download_progress_response_handler(
    response: DownloadProgressResponse,
) -> None:
    if not progress_bar.is_started:
        progress_bar.start(total=response.total)
    progress_bar.update(current=response.current)
    if response.is_complete:
        progress_bar.stop()


async def main() -> NoReturn:
    await client.start()
    await cli.start()


if __name__ == '__main__':
    run(main())
