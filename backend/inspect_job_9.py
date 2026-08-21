import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.models.schema import Job
from app.services.search import search_candidates

print("--- INSPECTING JOB 9 SEARCH ---")

db = SessionLocal()
job = db.query(Job).filter(Job.id == 9).first()

if not job:
    print("Job ID 9 not found in DB! Listing all available jobs in DB...")
    all_jobs = db.query(Job).all()
    for j in all_jobs:
        print(f"  Job ID {j.id}: '{j.title}' | Location: '{j.location}' | Skills: {j.skills}")
else:
    print(f"Found Job ID {job.id}: Title='{job.title}', Skills={job.skills}, Location='{job.location}'")
    print("\n--- RUNNING DIRECT SEARCH WITH DETAILED LOGGING ---")
    
    # Remove cache first to ensure live request
    from app.services.search import CACHE_FILE
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        
    res = search_candidates(job.title, job.skills, job.location)
    print("\nSearch Candidates Result Summary:")
    print(f"  Total Candidates Returned: {len(res.get('candidates', []))}")
    print(f"  Quota Exhausted Flag: {res.get('quota_exhausted')}")
    if res.get('candidates'):
        for idx, c in enumerate(res['candidates']):
            print(f"  [{idx+1}] Name: {c['name']} | Source: {c['source']} | Score: {c['match_score']}% | URL: {c['profile_url']}")
    else:
        print("  NO CANDIDATES RETURNED.")

db.close()
