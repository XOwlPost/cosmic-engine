from fabric import task

@task
def manage_snapshots(ctx, volume_path="/mnt/t7shield", retain_count=5):
    """
    Manages snapshots by creating a new one and retaining only the latest.
    """
    snapshot_name = f"snapshot-$(date +%F)"
    ctx.run(f"sudo btrfs subvolume snapshot {volume_path} {volume_path}/{snapshot_name}")
    snapshots = sorted(ctx.run(f"ls {volume_path}", hide=True).stdout.split())
    if len(snapshots) > retain_count:
        to_delete = snapshots[:-retain_count]
        for snap in to_delete:
            ctx.run(f"sudo btrfs subvolume delete {volume_path}/{snap}")
