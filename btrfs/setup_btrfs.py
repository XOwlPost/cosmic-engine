from fabric import task

@task
def setup_btrfs(ctx, device="/dev/sdb", mount_point="/mnt/t7shield"):
    """
    Sets up Btrfs on the specified device.
    """
    ctx.run(f"sudo mkfs.btrfs -f {device}")
    ctx.run(f"sudo mkdir -p {mount_point}")
    ctx.run(f"sudo mount {device} {mount_point}")
    uuid = ctx.run(f"blkid -s UUID -o value {device}", hide=True).stdout.strip()
    fstab_entry = f"UUID={uuid} {mount_point} btrfs defaults,compress=zstd 0 0"
    ctx.run(f"echo '{fstab_entry}' | sudo tee -a /etc/fstab")
    ctx.run("sudo mount -a")
