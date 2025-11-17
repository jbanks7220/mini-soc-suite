import platform

def normalize(logs):
    normalized = []

    if platform.system() == "Windows":
        return logs  # Already dicts

    # Linux syslog
    for line in logs:
        parts = line.split()
        if len(parts) < 5:
            continue
        normalized.append({
            "timestamp": " ".join(parts[:3]),
            "host": parts[3],
            "service": parts[4].replace(":", ""),
            "message": " ".join(parts[5:])
        })
    return normalized

