# =============================================================================
# main.py — Entry point for the Development Agent System
#
# What this does:
#   - Sets up logging for the entire application
#   - Schedules Module 1 (Commit Checker) to run daily at the configured time
#   - Keeps the process alive so the scheduler keeps running
#
# To run:  python main.py
# =============================================================================

import logging
from apscheduler.schedulers.blocking import BlockingScheduler

import config
from agents.commit_checker import run as run_commit_checker

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s  %(message)s",
    handlers=[
        logging.StreamHandler(),                      # Print to terminal
        logging.FileHandler("logs/agent.log"),        # Save to log file
    ]
)

logger = logging.getLogger(__name__)


def main():
    scheduler = BlockingScheduler(timezone="UTC")

    # Schedule Module 1 — Daily Commit Checker
    scheduler.add_job(
        func=run_commit_checker,
        trigger="cron",
        hour=config.COMMIT_CHECK_HOUR,
        minute=config.COMMIT_CHECK_MINUTE,
        id="commit_checker",
        name="Daily Commit Checker"
    )

    logger.info(
        f"Scheduler started. Commit check will run daily at "
        f"{config.COMMIT_CHECK_HOUR:02d}:{config.COMMIT_CHECK_MINUTE:02d} UTC."
    )
    logger.info("Press Ctrl+C to stop.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")


if __name__ == "__main__":
    main()
