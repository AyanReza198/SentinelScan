import subprocess
import re
import logging

def scan_ports(live_hosts: list[str], full_range: bool = False) -> dict:
    """
    Scan TCP ports on live hosts.
    Returns dictionary: { ip: [open_ports] }
    """

    results = {}

    for host in live_hosts:
        try:
            if full_range:
                command = ["nmap", "-sS", "-T4", "-p-", host]
            else:
                command = ["nmap", "-sS", "-T4", "--top-ports", "1000", host]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout

            open_ports = []

            # Match lines like: 22/tcp open ssh
            matches = re.findall(r"(\d+)/tcp\s+open", output)

            for port in matches:
                open_ports.append(int(port))

            results[host] = open_ports

        except subprocess.CalledProcessError:
            results[host] = []
            logging.error(f"Nmap error while scanning {host}")

    return results
