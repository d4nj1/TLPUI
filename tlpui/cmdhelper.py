def create_sudo_command(sudo: str, command: list[str]) -> list[str]:
    if sudo == "pkexec":
        # if user selection required do it via UI or nothing
        sudo_cmd = ["pkexec", "--disable-internal-agent"]
    else:
        sudo_cmd = [sudo]

    return sudo_cmd + command
