import asyncio
import logging
import subprocess
import sys
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_api_server():
    process = subprocess.Popen(
        [sys.executable, "run.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process


async def run_background_tasks():
    process = subprocess.Popen(
        [sys.executable, "run_tasks.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process


async def main():
    # Change to the server directory
    server_dir = Path(__file__).parent
    os.chdir(server_dir)

    # Start the API server
    api_process = await run_api_server()
    logger.info("API server started")

    # Start the background tasks
    tasks_process = await run_background_tasks()
    logger.info("Background tasks started")

    try:
        # Wait for both processes
        await asyncio.gather(
            asyncio.create_task(api_process.wait()),
            asyncio.create_task(tasks_process.wait())
        )
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        api_process.terminate()
        tasks_process.terminate()
        await asyncio.gather(
            asyncio.create_task(api_process.wait()),
            asyncio.create_task(tasks_process.wait())
        )


if __name__ == "__main__":
    asyncio.run(main()) 