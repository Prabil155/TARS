import subprocess


def get_cpu_info():
    result = subprocess.run(
        ["lscpu"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "Model name:" in line:
            return line.split(":", 1)[1].strip()

    return "CPU information not found."


def get_ram_info():
    result = subprocess.run(
        ["free", "-h"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if line.startswith("Mem:"):
            parts = line.split()

            return {
                "total": parts[1],
                "used": parts[2],
                "available": parts[6]
            }

    return "RAM information not found."


def get_disk_info():
    result = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    if len(lines) >= 2:
        parts = lines[1].split()

        return {
            "total": parts[1],
            "used": parts[2],
            "available": parts[3],
            "usage": parts[4]
        }

    return "Disk information not found."


def get_os_info():
    result = subprocess.run(
        ["lsb_release", "-ds"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout.strip()

    return "Operating system information not found."

