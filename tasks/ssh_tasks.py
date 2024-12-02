import os
import json
from fabric import task

@task
def setup_ssh(c, env=None):
    # Load configuration
    config_file = os.path.join("config", "ssh_config.json")
    if not os.path.exists(config_file):
        print(f"Configuration file {config_file} not found.")
        return

    with open(config_file, "r") as f:
        config = json.load(f)

    # Select environment
    if env not in config["environments"]:
        print(f"Invalid environment. Available: {', '.join(config['environments'].keys())}")
        return

    environment = config["environments"][env]
    target = f"{environment['user']}@{environment['host']}"

    ssh_dir = os.path.expanduser("~/.ssh")
    private_key = os.path.join(ssh_dir, "id_rsa")
    public_key = f"{private_key}.pub"

    # Step 1: Check if SSH keys exist
    if not os.path.exists(private_key):
        c.run(f'ssh-keygen -t rsa -b 2048 -f {private_key} -N ""')
        print("SSH key pair generated.")

    # Step 2: Ensure SSH agent is installed and running
    result = c.run("which ssh-agent", warn=True, hide=True)
    if result.failed:
        c.run("sudo apt update && sudo apt install -y openssh-client")
        print("SSH agent installed.")

    agent_check = c.run("pgrep ssh-agent", warn=True, hide=True)
    if agent_check.failed:
        c.run("eval $(ssh-agent -s)")
        print("SSH agent started.")

    # Step 3: Add private key to the agent
    key_check = c.run("ssh-add -l", warn=True, hide=True)
    if "no identities" in key_check.stdout:
        c.run(f"ssh-add {private_key}")
        print("Private key added to SSH agent.")

    # Step 4: Ensure proper permissions
    c.run(f"chmod 600 {private_key}")
    c.run(f"chmod 644 {public_key}")

    # Step 5: Copy public key to the target server
    c.run(f"ssh-copy-id -i {public_key} {target}")

    print(f"SSH setup completed successfully for {env} environment ({target})!")
