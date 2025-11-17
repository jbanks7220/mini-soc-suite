from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        log TEXT
    )
    """)
    conn.commit()
    conn.close()

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    logs = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    for l in logs:
        c.execute("INSERT INTO logs (timestamp, log) VALUES (?, ?)",
                  (str(datetime.datetime.now()), str(l)))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"}), 200


@app.route("/api/logs/latest")
def latest():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

