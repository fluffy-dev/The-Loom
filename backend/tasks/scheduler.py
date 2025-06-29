import asyncio
import logging

from backend.config.database.engine import db_helper
from backend.config.tasks import task_settings
from backend.tasks.service import CleanupService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def scheduled_cleanup_task():
    """
    A long-running task that periodically cleans up expired rooms.

    This function runs in an infinite loop, calling the CleanupService
    at a configured interval. It is designed to be started once on
    application startup.
    """
    logging.info("Cleanup scheduler started.")
    while True:
        try:
            async with db_helper.get_db_session() as session:
                cleanup_service = CleanupService(session)
                logging.info("Running scheduled cleanup of expired rooms.")
                await cleanup_service.find_and_delete_expired_rooms()
                logging.info("Cleanup finished.")
        except Exception as e:
            logging.error(f"An error occurred during cleanup: {e}")

        await asyncio.sleep(task_settings.CLEANUP_INTERVAL_SECONDS)