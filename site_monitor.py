import requests
import time
import hashlib

def fetch_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return hashlib.md5(response.content).hexdigest()
    except Exception as e:
        print(f"Error fetching the site: {e}")
        return None

def monitor_site(url, interval=60):
    last_hash = fetch_hash(url)
    if last_hash is None:
        print("Initial fetch failed. Exiting.")
        return

    print(f"Monitoring '{url}' every {interval} seconds.")
    while True:
        time.sleep(interval)
        current_hash = fetch_hash(url)
        if current_hash is None:
            continue
        if current_hash != last_hash:
            print(f"Change detected on {url}!")
            last_hash = current_hash
        else:
            print("No change detected.")

if __name__ == "__main__":
    website = input("Enter website URL to monitor: ")
    interval_sec = int(input("Enter check interval (in seconds): "))
    monitor_site(website, interval_sec)
