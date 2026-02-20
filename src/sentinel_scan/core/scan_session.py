import uuid
from datetime import datetime
import time
import logging

from sentinel_scan.core.target_handler import normalize_target
from sentinel_scan.core.host_discovery import discover_live_hosts
from sentinel_scan.core.port_scanner import scan_ports
from sentinel_scan.core.service_detector import detect_services
from sentinel_scan.output.csv_writer import write_findings
from sentinel_scan.output.summary_printer import print_summary


class ScanSession:
    def __init__(self, target_input: str, verbose: bool = False, full_range: bool = False):
        self.scan_id = self._generate_scan_id()
        self.timestamp = self._generate_timestamp()

        self.target_input = target_input
        self.verbose = verbose
        self.full_range = full_range

        self.normalized_targets = []
        self.live_hosts = []
        self.port_results = {}
        self.findings = []

        self.start_time = None
        self.end_time = None
        self.duration = None

    def _generate_scan_id(self) -> str:
        return f"scan_{uuid.uuid4().hex[:8]}"

    def _generate_timestamp(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run(self):
        self.start_time = time.time()

        logging.info(f"ScanSession {self.scan_id} started for target {self.target_input}")

        if self.verbose:
            print(f"[+] Starting ScanSession: {self.scan_id}")
            print(f"[+] Target Input: {self.target_input}")
            print(f"[+] Full Port Range: {'Yes' if self.full_range else 'No'}")
            print("")

        # Phase pipeline
        self._normalize_targets()
        self._discover_hosts()
        self._scan_ports()
        self._detect_services()

        write_findings(self)

        self.end_time = time.time()
        self.duration = round(self.end_time - self.start_time, 2)

        logging.info(f"ScanSession {self.scan_id} completed in {self.duration} seconds")
        logging.info(f"Total findings: {len(self.findings)}")

        print_summary(self)

        if self.verbose:
            print("")
            print(f"[+] Scan Completed: {self.scan_id}")
            print(f"[+] Duration: {self.duration} seconds")

    def _normalize_targets(self):
        try:
            self.normalized_targets = normalize_target(self.target_input)
            logging.info(f"Normalized targets: {self.normalized_targets}")

            if self.verbose:
                print(f"[+] Normalized Targets: {self.normalized_targets}")

        except Exception as e:
            logging.error(f"Target normalization failed: {e}")
            raise

    def _discover_hosts(self):
        try:
            self.live_hosts = discover_live_hosts(self.normalized_targets)
            logging.info(f"Live hosts discovered: {self.live_hosts}")

            if self.verbose:
                print(f"[+] Live Hosts Discovered: {self.live_hosts}")

        except Exception as e:
            logging.error(f"Host discovery failed: {e}")
            raise

    def _scan_ports(self):
        if not self.live_hosts:
            logging.info("No live hosts found. Skipping port scan.")

            if self.verbose:
                print("[+] No live hosts to scan.")
            return

        try:
            self.port_results = scan_ports(
                self.live_hosts,
                full_range=self.full_range
            )

            logging.info(f"Port scan results: {self.port_results}")

            if self.verbose:
                print(f"[+] Port Scan Results: {self.port_results}")

        except Exception as e:
            logging.error(f"Port scanning failed: {e}")
            raise

    def _detect_services(self):
        if not self.port_results:
            logging.info("No open ports found. Skipping service detection.")
            return

        try:
            self.findings = detect_services(self.port_results)
            logging.info(f"Service detection completed. Findings count: {len(self.findings)}")

            if self.verbose:
                print(f"[+] Service Detection Findings: {self.findings}")

        except Exception as e:
            logging.error(f"Service detection failed: {e}")
            raise
