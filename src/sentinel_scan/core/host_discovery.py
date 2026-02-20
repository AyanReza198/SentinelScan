import subprocess
import re
import logging

def discover_live_hosts(targets: list[str]) -> list[str]:
    """
    Perform host discovery using nmap ping scan.
    Returns list of live IP addresses.
    """

    live_hosts = []

    for target in targets:
        try:
            result = subprocess.run(
                ["nmap", "-sn", target],
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout

            # Match lines like:
            # Nmap scan report for 192.168.1.1
            # Nmap scan report for localhost (127.0.0.1)
            matches = re.findall(r"Nmap scan report for (.+)", output)

            for match in matches:
                # If IP is inside parentheses, extract it
                ip_match = re.search(r"\((.*?)\)", match)
                if ip_match:
                    live_hosts.append(ip_match.group(1))
                else:
                    live_hosts.append(match.strip())

        except subprocess.CalledProcessError:
            logging.error(f"Nmap error while scanning {host}")
            continue
            

    return list(set(live_hosts))
