import os
import time
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Extra fallback candidates
DEFAULT_LOGS = [
    "/var/log/syslog",
    "/var/log/auth.log",
    "/var/log/messages",
    "/var/log/kern.log",
    "/var/log/dmesg",
]


def autodetect_log_file(config):
    """
    Auto-selects the best available log file based on:
    1. log_candidates in config.yaml
    2. Fallback system logs (DEFAULT_LOGS)
    3. Creates agent_fallback.log if no logs exist
    """

    candidates = config.get("log_candidates", [])

    print("[+] Checking configured log candidates...")

    # Step 1: Try user-specified log files
    for log_path in candidates:
        if os.path.isfile(log_path):
            print(f"[+] Using found log file: {log_path}")
            return log_path
        else:
            print(f"[!] Not found: {log_path}")

    print("[!] No user-defined logs found. Trying default system logs...")

    # Step 2: Try known system logs
    for log_path in DEFAULT_LOGS:
        if os.path.isfile(log_path):
            print(f"[+] Using auto-detected log file: {log_path}")
            return log_path

    print("[!] No usable system logs found. Creating fallback log...")

    # Step 3: Create fallback
    fallback = "agent_fallback.log"
    with open(fallback, "a") as f:
        f.write("Initialized fallback log file.\n")

    print(f"[+] Fallback file created: {fallback}")
    return fallback


class LogHandler(FileSystemEventHandler):
    def __init__(self, logfile):
        self.logfile = logfile

    def on_modified(self, event):
        if event.src_path == self.logfile:
            try:
                with open(self.logfile, "r") as f:
                    lines = f.readlines()
                    if lines:
                        print(f"[LOG] {lines[-1].strip()}")
            except Exception as e:
                print(f"[Watcher Error] {e}")


def start_realtime_monitor(config):
    logfile = autodetect_log_file(config)

    if not os.path.isfile(logfile):
        print("[!] No readable logfile. Monitor exiting.")
        return

    print(f"[+] Starting real-time monitor for: {logfile}")

    handler = LogHandler(logfile)
    observer = Observer()

    directory = os.path.dirname(logfile) or "."
    observer.schedule(handler, path=directory, recursive=False)

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
