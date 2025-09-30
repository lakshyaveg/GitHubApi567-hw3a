from __future__ import annotations
import sys
import requests

BASE = "https://api.github.com"

class GitHubApiError(RuntimeError):
    pass

def _get_json(url: str, timeout: int = 15):
    """Small wrapper around requests.get that returns parsed JSON or raises."""
    try:
        r = requests.get(url, timeout=timeout)
    except requests.RequestException as exc:
        raise GitHubApiError(f"Network error calling {url}: {exc}") from exc

    if r.status_code == 404:
        raise GitHubApiError(f"404 from {url}")
    if r.status_code != 200:
        raise GitHubApiError(f"HTTP {r.status_code} from {url}: {getattr(r, 'text', '')}")
    return r.json()

def list_user_repos(user: str) -> list[str]:
    """Return repo names for a given user."""
    url = f"{BASE}/users/{user}/repos"
    repos = _get_json(url)
    # each repo item should have a "name" field
    return [item.get("name") for item in repos if "name" in item]

def repo_commits_count(user: str, repo: str) -> int:
    """Return the number of commits for a user's repo."""
    url = f"{BASE}/repos/{user}/{repo}/commits"
    commits = _get_json(url)
    return len(commits)

def repos_with_commit_counts(user: str) -> list[tuple[str, int]]:
    """[(repo_name, commit_count), ...]"""
    names = list_user_repos(user)
    return [(name, repo_commits_count(user, name)) for name in names]

def format_pairs(pairs: list[tuple[str, int]]) -> list[str]:
    """Format for the assignment-required lines."""
    return [f"Repo: {name} Number of commits: {count}" for name, count in pairs]

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m src.gh_api <github_user>", file=sys.stderr)
        return 2
    user = argv[1]
    lines = format_pairs(repos_with_commit_counts(user))
    for line in lines:
        print(line)
    return 0

if __name__ == "__main__":  # allow: python -m src.gh_api <user>
    raise SystemExit(main(sys.argv))
