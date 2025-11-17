import time
import yaml
from collector import collect_logs
from normalizer import normalize
from forwarder import send_to_siem
from watcher import start_realtime_monitor
from cli import cli

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_agent():
    config = load_config()
    args = cli()

    if args.realtime or config["use_realtime_monitoring"]:
        return start_realtime_monitor(config)

    print("[*] Mini-SOC Agent started (polling mode)")
    while True:
        logs = collect_logs(config)
        normalized = normalize(logs)
        send_to_siem(normalized, config)
        time.sleep(config["interval"])

if __name__ == "__main__":
    run_agent()

