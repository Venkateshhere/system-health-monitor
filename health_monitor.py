import psutil
import requests
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage("/").percent

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

results = [
    f"Timestamp: {timestamp}",
    f"CPU Usage: {cpu_usage}%",
    f"Memory Usage: {memory_usage}%",
    f"DISK Usage: {disk_usage}%",
]

alerts = []

if cpu_usage > CPU_THRESHOLD:
    alerts.append(f"CPU usage is high: {cpu_usage}%")

if memory_usage > MEMORY_THRESHOLD:
    alerts.append(f"Memory usage is high: {memory_usage}%")

if disk_usage > DISK_THRESHOLD:
    alerts.append(f"Disk usage is high: {disk_usage}%")

for a in alerts:
    results.append(f"ALERT: {a}")

for result in results:
    print(result)

with open("/home/ubuntu/system-health-monitor/monitor.log", "a") as log_file:
    for result in results:
        log_file.write(result + "\n")
    log_file.write("-" * 40 + "\n")

def send_slack_alert(alert_messages, timestamp):
    text = f"*System Health Alert* — `{timestamp}`\n" + "\n".join(f"• {m}" for m in alert_messages)
    payload = {"text": text}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        with open("/home/ubuntu/system-health-monitor/monitor.log", "a") as log_file:
            log_file.write(f"Slack alert failed: {e}\n")

if alerts:
    send_slack_alert(alerts, timestamp)
