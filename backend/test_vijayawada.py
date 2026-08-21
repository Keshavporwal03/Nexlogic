import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.search import search_candidates, get_fallback_cities

res = search_candidates(
    job_title="Software Engineer",
    required_skills=["Python", "React"],
    location="Vijayawada",
    experience="3 years",
    description="Looking for a Python developer"
)

for c in res['candidates']:
    print(f"- {c['name']} from {c['source']} ({c['location']}) - Score: {c['match_score']}")
