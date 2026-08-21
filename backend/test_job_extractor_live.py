import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(__file__))

from app.ai.job_extractor import extract_job_details

print("--- TESTING LIVE JOB DESCRIPTION EXTRACTION ---")

real_jd = """
We are seeking a Senior Full Stack Software Engineer to join our growing fintech team in Remote (US/Canada).

Requirements:
- 5+ years of software development experience building cloud-native web applications.
- Strong proficiency in Python, React, PostgreSQL, and AWS.
- Experience with Docker, Kubernetes, and CI/CD pipelines is a plus.
- Bachelor's degree in Computer Science or equivalent field.

Job Details:
- Salary range: $130,000 - $160,000 USD per year.
- Work mode: 100% Remote.
- Application deadline: October 31, 2026.
- Openings: 3 positions available.

Responsibilities:
Architect, build, and maintain high-throughput backend services and modern React user interfaces. Collaborate closely with product managers and security teams.
"""

try:
    extracted = extract_job_details(real_jd)
    print("\nExtraction Result:")
    for k, v in extracted.items():
        print(f"  {k}: {v}")

    assert extracted.get("title") is not None
    assert isinstance(extracted.get("skills"), list)
    assert len(extracted.get("skills")) > 0
    print("\nSUCCESS: Job details extracted cleanly without errors!")
except Exception as e:
    print(f"\nFAILED: {e}")
    sys.exit(1)

