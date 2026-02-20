import csv
import os


CSV_PATH = "data/scan_results.csv"

FIELDNAMES = [
    "scan_id",
    "timestamp",
    "target_input",
    "ip",
    "port",
    "protocol",
    "service",
    "version",
    "state"
]


def write_findings(scan_session):
    """
    Append findings to CSV.
    Prevent duplicates within same scan session.
    """

    if not scan_session.findings:
        return

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(CSV_PATH)

    # Deduplicate within same scan session
    unique_entries = {}
    for finding in scan_session.findings:
        key = (finding["ip"], finding["port"], finding["protocol"])
        unique_entries[key] = finding

    deduplicated_findings = list(unique_entries.values())

    with open(CSV_PATH, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        for finding in deduplicated_findings:
            writer.writerow({
                "scan_id": scan_session.scan_id,
                "timestamp": scan_session.timestamp,
                "target_input": scan_session.target_input,
                "ip": finding["ip"],
                "port": finding["port"],
                "protocol": finding["protocol"],
                "service": finding["service"],
                "version": finding["version"],
                "state": finding["state"]
            })
