import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

prompt = """
Extract job details from this text and return ONLY a JSON object:
Title: Senior Python Engineer
Location: Remote
Experience: 3+ years
Skills: Python, FastAPI, SQL
Description: Looking for an experienced engineer to build APIs.
"""

payload_with_fmt = {
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 500,
    "temperature": 0.1,
    "response_format": {"type": "json_object"}
}

payload_without_fmt = {
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 500,
    "temperature": 0.1
}

print("1. Testing WITH response_format...")
r1 = requests.post(API_URL, headers=headers, json=payload_with_fmt)
print("  Status:", r1.status_code)
if r1.status_code != 200:
    print("  Body:", r1.text)

print("\n2. Testing WITHOUT response_format...")
r2 = requests.post(API_URL, headers=headers, json=payload_without_fmt)
print("  Status:", r2.status_code)
if r2.status_code == 200:
    text = r2.json()["choices"][0]["message"]["content"]
    print("  Response text snippet:", text[:200])
