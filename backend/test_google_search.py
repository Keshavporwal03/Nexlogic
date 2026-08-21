import os
import sys
import time
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)



# Ensure backend root is in import path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.search import (
    search_serper_dev,
    search_candidates,
    _parse_candidate_name
)
import app.services.search as search_module
api_key = os.getenv("SERPER_API_KEY")
print(f"DEBUG: Loaded SERPER_API_KEY from .env: '{api_key[:10] if api_key else 'NONE'}'")
search_module.SERPER_API_KEY = api_key




print("--- TESTING SERPER.DEV SEARCH INTEGRATION ---")

# Test 1: Title Parsing
print("\n1. Testing Candidate Name Parsing from Search Result Titles...")
title1 = "Jane Doe - Senior React Developer - TechCorp | LinkedIn"
title2 = "John Smith | LinkedIn"
title3 = "LinkedIn Profile"

print("  Parsed 1:", _parse_candidate_name(title1))
print("  Parsed 2:", _parse_candidate_name(title2))
print("  Parsed 3:", _parse_candidate_name(title3))
assert _parse_candidate_name(title1) == "Jane Doe"
assert _parse_candidate_name(title2) == "John Smith"

# Test 2: Missing API credentials gracefulness
print("\n2. Testing Missing Credentials Behavior...")
with patch("app.services.search.SERPER_API_KEY", ""):
    res = search_serper_dev("Python Engineer", ["python", "fastapi"], "Remote")
    print("  Response when credentials missing:", res)
    assert res == {"candidates": [], "quota_exhausted": False}

# Test 3: Successful Serper Search & Parsing & 24h Caching
print("\n3. Testing Mocked Serper Search, Scoring, and 24h Caching...")
from app.services.search import CACHE_FILE
if os.path.exists(CACHE_FILE):
    os.remove(CACHE_FILE)

mock_response = MagicMock()
mock_response.status_code = 200
mock_response.json.return_value = {
    "organic": [
        {
            "title": "Alex Mercer - Lead Python & FastAPI Developer | LinkedIn",
            "link": "https://www.linkedin.com/in/alex-mercer-12345",
            "snippet": "Experienced Software Engineer specializing in Python, FastAPI, Postgres, Remote working..."
        },
        {
            "title": "Sam Taylor - Frontend Engineer | LinkedIn",
            "link": "https://www.linkedin.com/in/sam-taylor-67890",
            "snippet": "React, TypeScript, CSS developer located in London..."
        }
    ]
}

with patch("app.services.search.SERPER_API_KEY", "fake_key"), \
     patch("requests.post", return_value=mock_response) as mock_post:
    
    # First call: hits API
    res1 = search_serper_dev("Python Engineer", ["python", "fastapi"], "Remote")
    print("  First Call Candidates returned:", len(res1["candidates"]))
    print("  Candidate 0 details:", res1["candidates"][0])
    
    assert len(res1["candidates"]) == 2 # 2 raw search results returned
    c0 = res1["candidates"][0]
    c1 = res1["candidates"][1]
    assert c0["name"] == "Alex Mercer"
    assert c0["unverified"] is True
    assert c0["source"] == "Serper.dev (Public LinkedIn)"
    assert c0["match_score"] == 40.0 # Full match score
    assert c1["match_score"] == 0.0 # No skills/location match
    
    # Second call with same params: should hit 24-hour cache (no extra API call)
    res2 = search_serper_dev("Python Engineer", ["python", "fastapi"], "Remote")
    print("  Second Call Cached Result returned:", len(res2["candidates"]))
    assert mock_post.call_count == 1 # Verified cache hit!

# Test 4: Quota Limit (HTTP 403 / 429) Handling
print("\n4. Testing Quota Exhaustion (HTTP 403 / 429)...")
mock_quota_resp = MagicMock()
mock_quota_resp.status_code = 403
mock_quota_resp.json.return_value = {"message": "Not enough credits"}

with patch("app.services.search.SERPER_API_KEY", "fake_key"), \
     patch("requests.post", return_value=mock_quota_resp):
    
    res_quota = search_serper_dev("Unique Query For Quota Test", ["python"], "NY")
    print("  Quota Response:", res_quota)
    assert res_quota["quota_exhausted"] is True
    assert res_quota["candidates"] == []

# Test 5: LIVE Real API Call test with user's SERPER_API_KEY
print("\n5. Testing LIVE Real API Call to Serper.dev...")
from dotenv import load_dotenv
load_dotenv()
from app.services import search as search_module

if search_module.SERPER_API_KEY:
    print(f"  Found SERPER_API_KEY: {search_module.SERPER_API_KEY[:8]}...")
    # Clear cache before live call
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        
    live_res = search_serper_dev("Software Engineer", ["Python"], "Remote")
    print(f"  Live Call returned {len(live_res['candidates'])} candidates, quota_exhausted: {live_res['quota_exhausted']}")
    if live_res["candidates"]:
        for idx, cand in enumerate(live_res["candidates"][:3]):
            print(f"    Candidate {idx+1}: {cand['name']} | {cand['profile_url']} | Score: {cand['match_score']}%")
    else:
        print("  Note: Live call returned 0 candidates (check query or key balance).")
# Test 6: Verify low-score Serper candidate bypasses threshold filtering
print("\n6. Testing Low-Score Serper Candidate Threshold Bypass...")
from unittest.mock import MagicMock
from app.routers.candidates import run_candidate_search
from app.models.schema import Job

mock_db = MagicMock()
mock_job = Job(id=1, title="Developer", skills=["Python"], location="Remote", match_threshold=30.0)
mock_db.query.return_value.filter.return_value.first.return_value = mock_job

low_score_serper_cand = {
    "name": "Low Score Public Profile",
    "profile_url": "https://www.linkedin.com/in/low-score",
    "source": "Serper.dev (Public LinkedIn)",
    "skills": [],
    "location": "",
    "match_score": 15.0,  # Below threshold 30.0!
    "unverified": True
}

with patch("app.routers.candidates.search_candidates", return_value={"candidates": [low_score_serper_cand], "quota_exhausted": False}):
    router_res = run_candidate_search(job_id=1, db=mock_db)
    print("  Router returned candidates count:", len(router_res["candidates"]))
    print("  Candidate 0 score:", router_res["candidates"][0]["match_score"])
    assert len(router_res["candidates"]) == 1
    assert router_res["candidates"][0]["name"] == "Low Score Public Profile"
    print("  SUCCESS: Low-score Serper candidate bypassed 30.0 threshold gate!")

print("\n--- ALL TESTS PASSED SUCCESSFULLY! ---")

