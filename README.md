# EC2 System Health Monitor

A lightweight Python script that monitors CPU, memory, and disk usage on a Linux server, logs the results, and sends real-time alerts to Slack when usage crosses defined thresholds. Runs automatically every 5 minutes via cron.

## Features

- Tracks CPU, memory, and disk usage using `psutil`
- Configurable thresholds for each metric (default: 80%)
- Logs every run with a timestamp to `monitor.log`
- Sends a formatted alert to a Slack channel via Incoming Webhook when any threshold is breached
- Runs unattended on a schedule using cron
- Keeps secrets (Slack webhook URL) out of source control using environment variables

## Tech Stack

- Python 3
- [`psutil`](https://pypi.org/project/psutil/) — system resource metrics
- [`requests`](https://pypi.org/project/requests/) — Slack webhook delivery
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — environment variable management
- Slack Incoming Webhooks
- cron — scheduling
- AWS EC2 (Ubuntu) — deployment target

## How It Works

1. The script collects current CPU, memory, and disk usage percentages.
2. Each metric is compared against its threshold (default 80%).
3. Results are appended to `monitor.log` with a timestamp on every run.
4. If any threshold is breached, a formatted alert is posted to Slack via an Incoming Webhook.
5. A cron job triggers the script every 5 minutes, so monitoring runs continuously without manual intervention.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Venkateshhere/system-health-monitor.git
cd system-health-monitor
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure your Slack webhook

Copy the example env file and add your own webhook URL:

```bash
cp .env.example .env
```

Edit `.env` and set:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

(Create a webhook at [api.slack.com/apps](https://api.slack.com/apps) → your app → **Incoming Webhooks**.)

### 4. Run it manually to test

```bash
python3 health_monitor.py
```

You should see the current metrics printed and appended to `monitor.log`. If any threshold is breached, an alert will also post to Slack.

### 5. Automate with cron

```bash
crontab -e
```

Add:

```
*/5 * * * * /path/to/system-health-monitor/venv/bin/python3 /path/to/system-health-monitor/health_monitor.py >> /path/to/system-health-monitor/cron.log 2>&1
```

## Sample Output

```
Timestamp: 2026-09-09 11:33:58
CPU Usage: 0.0%
Memory Usage: 40.6%
DISK Usage: 72.1%
```

## Possible Improvements

- Add an alert cooldown so repeated breaches don't spam the same Slack channel every 5 minutes
- Add email (SES) as an alternative alert channel
- Track historical metrics for trend graphs
- Package as a systemd service instead of cron

## Author

Venkatesh Srinivasan — [github.com/Venkateshhere](https://github.com/Venkateshhere)
