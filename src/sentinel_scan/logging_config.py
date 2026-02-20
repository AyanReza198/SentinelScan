import logging
import os


LOG_DIR = "logs"
LOG_FILE = "sentinel_scan.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="a"
    )

    logging.info("Logging system initialized.")
