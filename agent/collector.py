import platform
import os

def detect_linux_log(candidates):
    """Return the first valid log file path from candidate list."""
    for path in candidates:
        if os.path.exists(path):
            print(f"[+] Using Linux log file: {path}")
            return path
    
    print("[!] No valid log file found. Agent will not run.")
    return None

def collect_linux_logs(path):
    if path is None or not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

def collect_windows_logs(log_name):
    import win32evtlog
    server = "localhost"
    logs = []

    handle = win32evtlog.OpenEventLog(server, log_name)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(handle, flags, 0)

    for ev in events:
        logs.append({
            "timestamp": str(ev.TimeGenerated),
            "event_id": ev.EventID,
            "source": ev.SourceName,
            "event_type": ev.EventType,
            "category": ev.EventCategory,
            "message": str(ev.StringInserts)
        })

    return logs

def collect_logs(config):
    if platform.system() == "Windows":
        return collect_windows_logs(config["windows_log"])

    # Auto-detect Linux log path
    log_file = detect_linux_log(config["log_candidates"])
    return collect_linux_logs(log_file)
