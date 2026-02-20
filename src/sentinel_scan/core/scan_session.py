import uuid
from datetime import datetime
import time
from sentinel_scan.core.target_handler import normalize_target


class ScanSession:
    def __init__(self, target_input: str, verbose: bool = False, full_range: bool = False):
        self.scan_id = self._generate_scan_id()
        self.timestamp = self._generate_timestamp()

        self.target_input = target_input
        self.verbose = verbose
        self.full_range = full_range

        self.normalized_targets = []
        self.live_hosts = []
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

        self.end_time = time.time()
        self.duration = round(self.end_time - self.start_time, 2)

        if self.verbose:
            print("")
            print(f"[+] Scan Completed: {self.scan_id}")
            print(f"[+] Duration: {self.duration} seconds")

    def _normalize_targets(self):
        self.normalized_targets = normalize_target(self.target_input)

        if self.verbose:
            print(f"[+] Normalized Targets: {self.normalized_targets}")

    # Placeholder methods (next building blocks will implement logic)
    def _discover_hosts(self):
        pass

    def _scan_ports(self):
        pass

    def _detect_services(self):
        pass
