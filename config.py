# =============================================================================
# config.py — Loads all credentials from .env file
# Do NOT put real secrets here — edit .env instead
# =============================================================================

import os
from dotenv import load_dotenv

load_dotenv()   # Reads .env file and injects values into os.environ

# --- GitHub ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- Team Members mapped to their individual repos ---
# .env format:  TEAM_REPOS=nikhil:nikhil/project-alpha,rahul:rahul/ecommerce-app
# Parsed into:  { "nikhil": "nikhil/project-alpha", "rahul": "rahul/ecommerce-app" }
TEAM_REPOS = {}
raw_team_repos = os.getenv("TEAM_REPOS", "")
for entry in raw_team_repos.split(","):
    entry = entry.strip()
    if ":" in entry:
        username, repo = entry.split(":", 1)
        TEAM_REPOS[username.strip()] = repo.strip()

# --- Email (SMTP) ---
EMAIL_SENDER     = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD   = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = [
    r.strip()
    for r in os.getenv("EMAIL_RECIPIENTS", "").split(",")
    if r.strip()
]
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# --- Scheduler ---
COMMIT_CHECK_HOUR   = int(os.getenv("COMMIT_CHECK_HOUR", 21))
COMMIT_CHECK_MINUTE = int(os.getenv("COMMIT_CHECK_MINUTE", 0))

# --- Log File Path ---
COMMIT_LOG_FILE = "logs/commit_log.json"
