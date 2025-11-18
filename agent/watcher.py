import os
import time
import platform
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEFAULT_LOGS = [
    "/var/log/syslog",
    "/var/log/auth.log",
    "/var/log/messages",
    "/var/log/kern.log",
]


def journald_available():
    """Check if systemd journal exists and journalctl is usable."""
    try:
        subprocess.run(
            ["journalctl", "-n", "1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except FileNotFoundError:
        return False


def tail_journald():
    """Continuously stream logs from journald."""
    print("[+] Using systemd journal as log source.")

    # -f = follow
    # -n 0 = don't print old logs
    cmd = ["journalctl", "-f", "-n", "0", "-o", "short"]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    print("[+] Journald stream started.\n")

    for line in process.stdout:
        clean = line.strip()
        if clean:
            print(f"[LOG] {clean}")


def autodetect_log_file(config):
    """Traditional file-based autodetect (fallback only now)."""
    candidates = config.get("log_candidates", [])

    print("[+] Checking configured log candidates...")

    for log_path in candidates:
        if os.path.isfile(log_path):
            print(f"[+] Found log file: {log_path}")
            return log_path

    print("[!] No configured log files found. Trying system defaults...")

    for log_path in DEFAULT_LOGS:
        if os.path.isfile(log_path):
            print(f"[+] Found default log file: {log_path}")
            return log_path

    return None


class LogHandler(FileSystemEventHandler):
    def __init__(self, logfile):
        self.logfile = logfile
        self.last_size = 0

    def on_modified(self, event):
        if event.src_path == self.logfile:
            try:
                with open(self.logfile, "r") as f:
                    f.seek(self.last_size)
                    new_data = f.read()
                    self.last_size = f.tell()

                for line in new_data.splitlines():
                    print(f"[LOG] {line.strip()}")

            except Exception as e:
                print(f"[Watcher Error] {e}")


def start_realtime_monitor(config):
    # 1. Try traditional log files
    logfile = autodetect_log_file(config)

    # 2. If none exist, use journald
    if logfile is None:
        if journald_available():
            print("[+] No log files found — switching to journald mode.")
            return tail_journald()

        # 3. If journald ALSO missing → fallback
        print("[!] No journald or log files. Creating fallback.")
        logfile = "agent_fallback.log"
        open(logfile, "a").close()

    # 4. Classic file monitoring mode
    print(f"[+] Monitoring file: {logfile}")

    handler = LogHandler(logfile)
    observer = Observer()
    observer.schedule(handler, os.path.dirname(logfile) or ".", recursive=False)

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
