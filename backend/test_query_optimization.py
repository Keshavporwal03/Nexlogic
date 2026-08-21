import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
key = os.getenv("SERPER_API_KEY")

url = "https://google.serper.dev/search"
headers = {"X-API-KEY": key, "Content-Type": "application/json"}

print("--- TESTING MULTI-CITY LOCATION HANDLING FOR JOB 9 ---")

# Multi-city string
location_raw = "Kanpur, Lucknow, Agra, Prayagraj, Noida"
first_city = location_raw.split(",")[0].strip()

queries = [
    f'site:linkedin.com/in "Financial Manager" "{first_city}"',
    'site:linkedin.com/in "Financial Manager" Lucknow',
    'site:linkedin.com/in "Financial Manager" Noida'
]

for q in queries:
    res = requests.post(url, headers=headers, json={"q": q})
    items = res.json().get("organic", [])
    print(f"Query: '{q}' -> {len(items)} items returned.")
    if items:
        for item in items[:2]:
            print(f"  - {item.get('title')} -> {item.get('link')}")
