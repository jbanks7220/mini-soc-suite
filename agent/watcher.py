import platform
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from collector import detect_linux_log, collect_linux_logs
from normalizer import normalize
from forwarder import send_to_siem


class LogHandler(FileSystemEventHandler):
    def __init__(self, path, config):
        self.path = path
        self.config = config

    def on_modified(self, event):
        if event.src_path == self.path:
            logs = collect_linux_logs(self.path)
            normalized = normalize(logs[-10:])
            send_to_siem(normalized, self.config)


def start_realtime_monitor(config):
    if platform.system() == "Windows":
        print("[!] Real-time monitoring only supported for Linux.")
        return

    # Auto-detect log file
    log_file = detect_linux_log(config["log_candidates"])
    
    if log_file is None:
        print("[!] No valid log file found. Real-time monitor exiting.")
        return

    if not os.path.isfile(log_file):
        print(f"[!] Log file is not a file: {log_file}")
        return

    print(f"[+] Starting real-time monitoring on: {log_file}")

    event_handler = LogHandler(log_file, config)
    observer = Observer()

    # Watch the directory containing the log file
    directory = os.path.dirname(log_file)
    observer.schedule(event_handler, path=directory, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("[*] Stopped real-time monitoring.")

    observer.join()
