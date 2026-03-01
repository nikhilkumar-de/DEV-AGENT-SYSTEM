# =============================================================================
# utils/github_client.py — GitHub API connection wrapper
# Accepts a repo_name so it can connect to ANY repo dynamically
# Used by all three modules
# =============================================================================

from github import Github
import config


def get_repo(repo_name: str):
    """
    Connect to GitHub using the token from config and return the repo object.

    Args:
        repo_name: The full repo name e.g. "nikhil/project-alpha"

    Returns:
        A PyGitHub Repository object for that specific repo.
    """
    client = Github(config.GITHUB_TOKEN)
    repo   = client.get_repo(repo_name)
    return repo
