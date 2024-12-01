from fabric import task
from btrfs.setup_btrfs import setup_btrfs
from btrfs.snapshot_management import manage_snapshots

@task
def deploy_cosmic_tasks(ctx):
    print("Deploying cosmic tasks...")
    setup_btrfs(ctx, device="/dev/sdb", mount_point="/mnt/t7shield")
    manage_snapshots(ctx)
