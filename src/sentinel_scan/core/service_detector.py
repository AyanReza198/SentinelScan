import subprocess
import re
import logging


def detect_services(port_results: dict) -> list[dict]:
    """
    Perform service and version detection on open ports.
    Returns list of structured findings.
    """

    findings = []

    for host, ports in port_results.items():
        if not ports:
            continue

        port_string = ",".join(str(p) for p in ports)

        try:
            result = subprocess.run(
                ["nmap", "-sV", "-p", port_string, host],
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout

            # Match lines like:
            # 22/tcp open  ssh  OpenSSH 8.4
            matches = re.findall(
                r"(\d+)/tcp\s+open\s+(\S+)\s*(.*)",
                output
            )

            for port, service, version in matches:
                findings.append({
                    "ip": host,
                    "port": int(port),
                    "protocol": "tcp",
                    "service": service.strip(),
                    "version": version.strip(),
                    "state": "open"
                })

        except subprocess.CalledProcessError:
            logging.error(f"Nmap error while scanning {host}")
            continue
            
    return findings
