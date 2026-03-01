# =============================================================================
# agents/commit_checker.py — Module 1: Daily Commit Checker
#
# What this does:
#   1. Loops through each team member and their individual repo
#   2. Checks if that member made at least one commit today in their own repo
#   3. Sends an Email alert for each member who has NOT committed
#   4. Appends the daily result to logs/commit_log.json
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging
from datetime import datetime, timezone

import config
from utils.github_client import get_repo
from utils.notifier import send_email

logger = logging.getLogger(__name__)


def has_committed_today(username: str, repo_name: str) -> bool:
    """
    Check if a specific team member has made at least one commit
    today in their own repository.

    Args:
        username  : GitHub username of the team member
        repo_name : Full repo name e.g. "nikhil/project-alpha"

    Returns:
        True if they committed today, False otherwise.
    """
    today_midnight = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    try:
        repo    = get_repo(repo_name)
        commits = repo.get_commits(since=today_midnight)

        for commit in commits:
            # Check GitHub user object first, fallback to raw git author name
            committer = (
                commit.author.login
                if commit.author
                else commit.commit.author.name
            )
            if committer == username:
                logger.info(f"{username} has committed today in {repo_name}")
                return True

        logger.info(f"{username} has NOT committed today in {repo_name}")
        return False

    except Exception as e:
        logger.error(f"Error checking repo {repo_name} for {username}: {e}")
        return False   # Treat errors as "not committed" to be safe


def send_alert(username: str, repo_name: str):
    """
    Send an email alert for a team member who has not committed today.
    """
    today_str = datetime.now().strftime("%b %d, %Y")
    subject   = f"Commit Alert: {username} has not committed today ({today_str})"
    body      = (
        f"Hello Team,\n\n"
        f"This is an automated alert from the Development Agent System.\n\n"
        f"Team member  : {username}\n"
        f"Repository   : {repo_name}\n"
        f"Date         : {today_str}\n"
        f"Status       : No commit found today.\n\n"
        f"Please follow up with {username} to check on their progress.\n\n"
        f"-- Development Agent System"
    )
    send_email(subject=subject, body=body)


def log_result(results: list):
    """
    Append today's full commit check result to logs/commit_log.json.

    results is a list of dicts:
    [
      { "username": "nikhil", "repo": "nikhil/project-alpha", "committed": True  },
      { "username": "rahul",  "repo": "rahul/ecommerce-app",  "committed": False },
      ...
    ]
    """
    log_entry = {
        "date"       : datetime.now().strftime("%Y-%m-%d"),
        "check_time" : datetime.now().strftime("%H:%M:%S"),
        "results"    : results,
        "total_checked"   : len(results),
        "total_committed" : sum(1 for r in results if r["committed"]),
        "total_missing"   : sum(1 for r in results if not r["committed"]),
    }

    log_file = config.COMMIT_LOG_FILE
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Log written to {log_file}")


def run():
    """
    Main entry point for Module 1.
    Loops through every member in TEAM_REPOS and checks their individual repo.
    Called by the scheduler in main.py every day at the configured time.
    """
    logger.info("=== Module 1: Daily Commit Checker started ===")
    logger.info(f"Checking {len(config.TEAM_REPOS)} team member(s)...")

    results      = []
    alert_count  = 0

    for username, repo_name in config.TEAM_REPOS.items():
        committed = has_committed_today(username, repo_name)

        results.append({
            "username"  : username,
            "repo"      : repo_name,
            "committed" : committed,
        })

        if not committed:
            send_alert(username, repo_name)
            alert_count += 1

    if alert_count == 0:
        logger.info("All team members have committed today. No alerts sent.")
    else:
        logger.info(f"Alerts sent for {alert_count} member(s).")

    log_result(results)

    logger.info("=== Module 1: Daily Commit Checker finished ===")


# --- Manual test: run this file directly to test without the scheduler ---
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)s  %(message)s"
    )
    run()
