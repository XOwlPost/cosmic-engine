from tasks.git_tasks import validate_commits, update_spec
from tasks.ssh_tasks import setup_ssh
from fabric import task
from btrfs.setup_btrfs import setup_btrfs
from btrfs.snapshot_management import manage_snapshots
import os

@task
def deploy_cosmic_tasks(ctx):
    print("Deploying cosmic tasks...")
    setup_btrfs(ctx, device="/dev/sdb", mount_point="/mnt/t7shield")
    manage_snapshots(ctx)

@task
def deploy_repo(c, repo_url="git@github.com:XOwlPost/cosmic-engine.git", branch="main"):
    """
    Clones or updates the repo and sets up SSH for Git operations.
    """
    project_dir = "~/cosmic-engine"
    if not c.run(f"test -d {project_dir}", warn=True).ok:
        c.run(f"git clone {repo_url} {project_dir}")
    else:
        c.run(f"cd {project_dir} && git fetch && git checkout {branch} && git pull")
    c.run(f"cd {project_dir} && git remote set-url origin {repo_url}")
    print("Repository deployed and ready!")
