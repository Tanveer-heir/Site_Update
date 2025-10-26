import requests
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import argparse
import os
import sys

def fetch_hash(url, algo):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        hash_func = getattr(hashlib, algo)
        return hash_func(response.content).hexdigest(), response.content
    except Exception as e:
        print(f"[{datetime.now()}] Error fetching the site: {e}")
        return None, None

def send_email_change(url, email, password, to_email):
    try:
        msg = MIMEText(f"Change detected on {url} at {datetime.now()}")
        msg['Subject'] = f"[Website Monitor] Change detected: {url}"
        msg['From'] = email
        msg['To'] = to_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
        print(f"[{datetime.now()}] Email notification sent.")
    except Exception as e:
        print(f"[{datetime.now()}] Error sending email: {e}")

def log_event(log_file, message):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def save_snapshot(folder, content, suffix=""):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{folder}/{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}.html"
    with open(filename, "wb") as f:
        f.write(content)
    print(f"[{datetime.now()}] Snapshot saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Website Change Monitor")
    parser.add_argument('--url', required=True, help='Website URL to monitor')
    parser.add_argument('--interval', type=int, default=60, help='Check interval (seconds)')
    parser.add_argument('--log', default="monitor.log", help='Log file path')
    parser.add_argument('--algo', default="md5", choices=hashlib.algorithms_available, help='Hash algorithm: md5/sha1/sha256/...')
    parser.add_argument('--email', help='Sender Gmail for notifications')
    parser.add_argument('--password', help='Sender Gmail App Password')
    parser.add_argument('--to', help='Recipient email for notifications')
    parser.add_argument('--snapshots', default="snapshots", help='Directory to save snapshots')
    args = parser.parse_args()

    change_count = 0
    check_count = 0

    log_event(args.log, f"Started monitoring: {args.url}")
    hash_val, content = fetch_hash(args.url, args.algo)
    if hash_val is None:
        log_event(args.log, "Initial fetch failed. Exiting.")
        print("Initial fetch failed. Exiting.")
        sys.exit(1)

    save_snapshot(args.snapshots, content, suffix="_initial")
    log_event(args.log, f"Initial hash {args.algo.upper()}: {hash_val}")

    print(f"Monitoring '{args.url}' every {args.interval} seconds (hash: {args.algo.upper()})")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(args.interval)
            check_count += 1
            current_hash, current_content = fetch_hash(args.url, args.algo)
            if current_hash is None:
                log_event(args.log, "Fetch error during monitoring.")
                continue
            if current_hash != hash_val:
                msg = f"Change detected! Old hash: {hash_val}, New hash: {current_hash}"
                log_event(args.log, msg)
                print(msg)
                change_count += 1
                save_snapshot(args.snapshots, current_content, suffix="_change")
                if all([args.email, args.password, args.to]):
                    send_email_change(args.url, args.email, args.password, args.to)
                hash_val = current_hash
            else:
                msg = "No change detected."
                log_event(args.log, msg)
                print(msg)
    except KeyboardInterrupt:
        log_event(args.log, "Monitoring stopped by user.")
        print(f"\nMonitoring stopped. {check_count} checks performed, {change_count} changes found.")
        print(f"Log file: {args.log}")
        print(f"Snapshots stored in: {args.snapshots}")

if __name__ == "__main__":
    main()
