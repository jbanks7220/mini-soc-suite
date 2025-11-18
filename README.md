# 🛰️ Mini-SOC Suite
## Cross-Platform Log Collection Agent + Forwarder + Minimal SIEM Backend
---  
**Mini-SOC Suite is a small, fully functional Security Operations Center (SOC) pipeline designed for learning, demonstration, and portfolio use.**  
It simulates the core components of an enterprise SIEM:  

* A Log Collection Agent (runs on Windows + Linux)  

* Real-time log monitoring  

* Automatic log source detection  

* JSON normalization  

* Secure HTTP forwarding  

* A Flask-based SIEM ingestion API  

* SQLite storage for ingested events  

**This project demonstrates the skills used in real-world SIEM, SOC, and security engineering roles—packaged into a clean, easy-to-run project for recruiters and interviewers.**

## 🔎 Why This Project Matters

**Security engineers, SOC analysts, and detection engineers routinely work with:**

Distributed agents  

Log normalization pipelines  

SIEM data ingestion  

System logging frameworks (auth.log, syslog, journald, Windows Event Log)  

API design  

Fault-tolerant event forwarding  

Mini-SOC Suite demonstrates all of this in a compact project you can explain clearly in interviews.  

Recruiters and hiring managers can understand its purpose at a glance, and technical reviewers can dig into the code to see your engineering capability.  

## 🎯 Project Goals

**The project replicates the primary flow of a modern SIEM:**

  [OS Logs] → [Agent] → JSON → [Transport] → HTTP → [SIEM API] → SQLite

**✔ Cross-platform log collection**

Linux (auth.log, syslog, journalctl)  

Windows (Security/System/Application logs)  

**✔ Real-time monitoring**

Watches files  

Streams systemd-journal on modern systems  

Uses watchdog or subprocess streaming  

**✔ Log normalization**  

Converts raw logs into structured, SIEM-friendly JSON.  

**✔ Forwarding + Reliability**  

HTTP POST to SIEM backend  

Automatic retry  

Backoff delay  

Fallback local logging  

**✔ Minimal SIEM backend**

Flask API endpoint  

Stores logs in SQLite  

Prints events to terminal for live monitoring  

## 🧩 Architecture Overview  

                           ┌─────────────────────┐
                           │   Mini-SOC Agent     │
                           │  (Windows / Linux)   │
                           └─────────────────────┘
                                      │
                         Real-time OS log monitoring
                                      │
                                      ▼
                     ┌────────────────────────────────┐
                     │  Normalized JSON log payloads  │
                     └────────────────────────────────┘
                                      │
                                   HTTP POST
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │     SIEM API Backend   │
                        │   (Flask + SQLite DB)  │
                        └────────────────────────┘

## 🖥️ Components
🔹 1. Log Collection Agent (agent/)  

A cross-platform Python service that:  

Identifies available logs automatically  

Selects the best available source  

Handles journald, classic /var/log/* files, and Windows logs  

Normalizes each event into structured JSON  

Sends logs to the SIEM backend  

Designed to behave like a lightweight Splunk Forwarder or Elastic Beats agent.  

🔹 2. SIEM API Backend (SIEM-api/)  

A minimal Flask API that:  

Accepts POSTed log events  

Stores them in a SQLite database  

Prints them to console for demonstration  

This allows recruiters/interviewers to see the full pipeline working live.  

## ⚙️ Installation
```
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/mini-soc-suite
cd mini-soc-suite
```

## 🚀 Running the SIEM Backend
```
cd SIEM-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python api.py
```

**You should see:**
```

[+] SIEM API running on http://0.0.0.0:5000

🛰️ Running the Log Agent
```

Open a second terminal:
```
cd agent
python3 main.py
```

Expected log messages:
```
[+] Checking configured log candidates...
[+] No traditional logs found — switching to journald mode.
[+] Journald stream started.
[LOG] Jan 18 20:14:11 sshd[5121]: Failed password for root …
```

## 🧪 Testing the Pipeline  

**Linux Test**

Trigger SSH failures:
```
ssh fakeuser@localhost
```

Or sudo:
```
sudo -k
sudo ls
```
Windows Test
```
eventcreate /ID 100 /L APPLICATION /T INFORMATION /SO Test /D "Mini-SOC Event"
```

Events should appear instantly in the SIEM terminal.

📁 Config File (agent/config.yaml)

Example:
```
api_url: "http://localhost:5000/api/logs"
interval: 10

log_candidates:
  - "/var/log/auth.log"
  - "/var/log/secure"
  - "/var/log/syslog"

windows_log: "Security"

retry_attempts: 3
retry_delay: 2

use_realtime_monitoring: true
```
