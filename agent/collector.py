import platform
import os

def collect_linux_logs(path):
    if not os.path.exists(path):
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
    else:
        return collect_linux_logs(config["log_path_linux"])

