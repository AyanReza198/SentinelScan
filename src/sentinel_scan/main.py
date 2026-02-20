import argparse
import sys

from sentinel_scan.core.scan_session import ScanSession
from sentinel_scan.logging_config import setup_logging
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="SentinelScan",
        description="SentinelScan - Recon & Enumeration Engine (Phase 1)"
    )

    parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Target IP, CIDR range, or domain"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--full-range",
        action="store_true",
        help="Scan full TCP port range (1-65535)"
    )

    return parser.parse_args()


def main():

    setup_logging()
    logging.info("SentinelScan started.")
    
    args = parse_arguments()

    try:
        session = ScanSession(
            target_input=args.target,
            verbose=args.verbose,
            full_range=args.full_range
        )

        session.run()

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(1)

    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
