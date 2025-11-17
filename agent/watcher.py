from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collector import collect_linux_logs
from normalizer import normalize
from forwarder import send_to_siem
import time
import platform

class LogHandler(FileSystemEventHandler):
    def __init__(self, path, config):
        self.path = path
        self.config = config

    def on_modified(self, event):
        if event.src_path == self.path:
            logs = collect_linux_logs(self.path)
            normalized = normalize(logs[-10:])  # last 10 lines
            send_to_siem(normalized, self.config)

def start_realtime_monitor(config):
    if platform.system() == "Windows":
        print("[!] Real-time monitoring only supports Linux for now.")
        return

    path = config["log_path_linux"]
    event_handler = LogHandler(path, config)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print("[*] Real-time monitoring started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

