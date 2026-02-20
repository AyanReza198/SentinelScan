from collections import Counter


def print_summary(scan_session):
    """
    Print human-readable summary of scan results.
    """

    print("\n" + "=" * 50)
    print("SentinelScan - Phase 1 Summary")
    print("=" * 50)

    print(f"Scan ID: {scan_session.scan_id}")
    print(f"Target: {scan_session.target_input}")
    print(f"Timestamp: {scan_session.timestamp}")
    print("")

    live_host_count = len(scan_session.live_hosts)
    total_ports = len(scan_session.findings)

    print(f"Live Hosts Discovered: {live_host_count}")
    print(f"Total Open Services: {total_ports}")
    print("")

    if scan_session.findings:
        services = [finding["service"] for finding in scan_session.findings]
        service_counts = Counter(services)

        print("Services Identified:")
        for service, count in service_counts.items():
            print(f" - {service} ({count})")
    else:
        print("No open services identified.")

    print("")
    print(f"Scan Duration: {scan_session.duration} seconds")
    print("Results appended to: data/scan_results.csv")
    print("=" * 50 + "\n")
