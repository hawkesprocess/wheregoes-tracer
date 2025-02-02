import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time
import traceback
import threading

DISCORD_WEBHOOK_URL = "Your Discord Webhook" #Change to your webhook
TRIGGER_KEYWORDS = ["keyword1", "keyword2", "keyword3", "keyword4"] #Change to your choice of keyword

def send_to_discord_embed(trace_url, status_links, date_traced):
    content_text = "\n".join(status_links)
    if not any(keyword.lower() in content_text.lower() for keyword in TRIGGER_KEYWORDS):
        return
    mention = "@everyone\n"
    singapore_tz = pytz.timezone('Asia/Singapore')
    current_time = datetime.now(singapore_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
    embed = {
        "title": "Wheregoes Tracer",
        "description": trace_url,
        "color": 3447003,
        "fields": [
            {"name": "Date Traced", "value": date_traced, "inline": False},
            {"name": "Status Code Links", "value": content_text, "inline": False}
        ],
        "footer": {"text": f"Scraped at {current_time}"}
    }
    payload = {"content": mention, "embeds": [embed]}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code not in (200, 204):
            print(f"Failed to send embed to Discord: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error sending embed to Discord: {e}")

def scrape_page(page_id):
    url = f"https://wheregoes.com/trace/{page_id}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            results = []
            for a in soup.find_all("a", class_=re.compile("^code-")):
                status = a.get_text(strip=True)
                textarea = a.find_next("textarea", class_="hide copy-url")
                if textarea:
                    raw_url = textarea.get_text(strip=True)
                    cleaned_url = raw_url.replace("|", "")
                    results.append(f"{status} -> {cleaned_url}")
            date_traced_tag = soup.find("p", class_="date")
            date_traced = date_traced_tag.get_text(strip=True) if date_traced_tag else "N/A"
            return results if results else None, date_traced
        else:
            print(f"Page {page_id} returned status code {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error scraping page {page_id}: {e}")
        return None, None

def scrape_and_send(page_id):
    trace_url = f"https://wheregoes.com/trace/{page_id}/"
    print(f"Scraping {trace_url}")
    status_links, date_traced = scrape_page(page_id)
    if status_links:
        send_to_discord_embed(trace_url, status_links, date_traced)
    else:
        print(f"No valid content found for {trace_url}. Skipping webhook.")

def main_loop():
    page_id = 2025773308 # Change it as you deem fit
    while True:
        threads = []
        for i in range(50):
            thread = threading.Thread(target=scrape_and_send, args=(page_id + i,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        page_id += 50
        time.sleep(10)

def keep_alive():
    while True:
        try:
            main_loop()
        except Exception as e:
            print("Unhandled exception occurred. Restarting in 5 seconds...")
            traceback.print_exc()
            time.sleep(5)

if __name__ == "__main__":
    keep_alive()
