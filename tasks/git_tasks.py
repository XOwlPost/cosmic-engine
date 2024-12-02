import subprocess
import re
import requests
from fabric import task

# Global regex pattern for Conventional Commits
CONVENTIONAL_COMMIT_REGEX = (
    r"^(feat|fix|chore|docs|refactor|test|build|ci|perf|style)(\(.+\))?: .+$"
)

@task
def validate_commits(c, auto_fix=False):
    """
    Validate recent Git commit messages against Conventional Commits.
    Optionally auto-fix invalid messages.
    """
    # Fetch the latest 10 commits
    result = c.run("git log -n 10 --pretty=format:'%h %s'", hide=True, warn=True)
    if result.failed:
        print("Failed to fetch Git commit logs.")
        return

    # Parse commit messages
    commits = result.stdout.split("\n")
    for commit in commits:
        commit_hash, commit_message = commit.split(" ", 1)
        if not re.match(CONVENTIONAL_COMMIT_REGEX, commit_message):
            print(f"❌ Invalid commit message: {commit_hash} - {commit_message}")
            if auto_fix:
                # Attempt to auto-fix based on the message content
                new_message = auto_format_message(commit_message)
                if new_message:
                    c.run(f"git commit --amend -m '{new_message}'")
                    print(f"✅ Commit {commit_hash} message auto-fixed to: {new_message}")
                else:
                    print(f"⚠️ Unable to auto-fix commit: {commit_message}")
            else:
                print(
                    "Commit message does not follow Conventional Commits. "
                    "Expected format: <type>(<scope>): <description>\n"
                    "Example: feat(auth): add user login functionality"
                )
        else:
            print(f"✅ Valid commit: {commit_hash} - {commit_message}")

    print("Commit validation completed.")

def auto_format_message(message):
    """
    Attempt to reformat a non-compliant commit message into a Conventional Commit.
    """
    # Simple heuristic to determine commit type from keywords
    if "fix" in message.lower():
        return f"fix: {message}"
    elif "add" in message.lower() or "create" in message.lower():
        return f"feat: {message}"
    elif "update" in message.lower() or "refactor" in message.lower():
        return f"refactor: {message}"
    elif "doc" in message.lower():
        return f"docs: {message}"
    elif "test" in message.lower():
        return f"test: {message}"
    elif "initial" in message.lower() and "commit" in message.lower():
        return "chore: Initial commit"
    return None

@task
def update_spec(c):
    """
    Check for updates to the Conventional Commits specification and apply changes.
    """
    spec_url = "https://www.conventionalcommits.org/en/v1.0.0/"
    try:
        response = requests.get(spec_url)
        if response.status_code == 200:
            print("Conventional Commits specification is up-to-date.")
            # Optionally parse the content to identify changes and update regex
            # Example: Extract new keywords, types, or examples
        else:
            print(f"Failed to fetch specification. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error checking specification: {e}")

    print("Specification update completed.")
