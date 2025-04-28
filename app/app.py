from flask import Flask, render_template
import subprocess
from datetime import datetime
import pytz
import re

app = Flask(__name__, template_folder='templates')

hosts = [
    {"name": "Google DNS", "ip": "8.8.8.8"},
    {"name": "Cloudflare DNS", "ip": "1.1.1.1"},
    {"name": "Localhost", "ip": "127.0.0.1"}
]

def check_ping(ip):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", "-W", "2", ip],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        # Extract ping time (example: time=21.5 ms)
        match = re.search(r'time=(\d+\.?\d*) ms', output)
        if match:
            ping_time = match.group(1) + " ms"
        else:
            ping_time = "N/A"
        return True, ping_time
    except subprocess.CalledProcessError:
        return False, None

@app.route('/')
def home():
    statuses = []
    for host in hosts:
        status, ping_time = check_ping(host["ip"])
        statuses.append({
            "name": host["name"],
            "ip": host["ip"],
            "status": status,
            "ping_time": ping_time
        })
    israel_time = datetime.now(pytz.timezone('Asia/Jerusalem')).strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', hosts=statuses, reload_time=israel_time)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
