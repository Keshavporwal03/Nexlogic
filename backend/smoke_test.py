import os
import time
import requests
import subprocess
from dotenv import load_dotenv
load_dotenv()
from app.ai.banner_gen import create_job_banner
from app.ai.post_gen import filter_profanity
from app.database.connection import SessionLocal
from app.models.schema import Job

print("--- SMOKE TEST START ---")

print("\n1. Testing DB connection directly...")
try:
    db = SessionLocal()
    # just query jobs to ensure connection works
    db.query(Job).first()
    print("DB Connection OK.")
    db.close()
except Exception as e:
    print(f"DB Connection Failed: {e}")

print("\n2. Testing Banner Generation API (Real Hugging Face Call)...")
try:
    job_details = {"title": "Software Engineer", "experience": "3+ Years", "location": "Remote"}
    colors = {"primary_color": "#384F3E", "background_color": "#F9F6F2", "text_color": "#1F1F1F"}
    banner_bytes = create_job_banner(job_details, colors)
    if len(banner_bytes.getvalue()) > 0:
        print("Banner generation (fallback) OK. Bytes generated:", len(banner_bytes.getvalue()))
    else:
        print("Banner generation failed.")
except Exception as e:
    print(f"Banner test failed: {e}")

print("\n3. Starting FastAPI Server...")
import sys
proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"])

time.sleep(5)

print("\n4. Testing Swagger UI...")
try:
    r = requests.get("http://localhost:8000/docs")
    if r.status_code == 200:
        print("Swagger UI OK.")
    else:
        print(f"Swagger UI Failed: {r.status_code}")
except Exception as e:
    print(f"Swagger UI Failed: {e}")

print("\n5. Testing Candidate Search Endpoint...")
try:
    # We need a job in DB to test the search endpoint.
    db = SessionLocal()
    job = Job(title="Test Job", skills=["python"], location="remote")
    db.add(job)
    db.commit()
    job_id = job.id
    db.close()
    
    r = requests.post(f"http://localhost:8000/candidates/search/{job_id}")
    if r.status_code == 200:
        print("Candidate Search Endpoint OK. Response summary:", len(r.json().get('candidates', [])))
    else:
        print(f"Candidate Search Endpoint Failed: {r.status_code} - {r.text}")
except Exception as e:
    print(f"Candidate Search Endpoint Failed: {e}")

print("\nCleaning up...")
proc.terminate()
print("--- SMOKE TEST END ---")
