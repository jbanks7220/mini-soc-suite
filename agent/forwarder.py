import requests
import time
import json

def send_to_siem(json_logs, config):
    url = config["api_url"]
    attempts = config["retry_attempts"]
    delay = config["retry_delay"]

    for i in range(attempts):
        try:
            r = requests.post(url, json=json_logs)
            if r.status_code == 200:
                print("[+] Logs sent successfully")
                return True
            print(f"[-] API Error: {r.status_code}")
        except Exception as e:
            print(f"[-] Send attempt {i+1} failed: {e}")
        time.sleep(delay)

    print("[!] Max retry attempts reached")
    return False

