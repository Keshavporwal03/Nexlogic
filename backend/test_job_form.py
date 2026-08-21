import os
import requests

url = "http://127.0.0.1:8000/jobs"

# Test payload without deadline or match_threshold, with mandatory skills & education_requirements
payload = {
    "title": "Senior Cloud Security Engineer",
    "experience": "5+ Years",
    "min_experience": 5,
    "max_experience": 8,
    "location": "Noida, UP",
    "remote_type": "On-site",
    "skills": ["AWS Security", "Terraform", "Python", "Kubernetes"],
    "education_requirements": ["B.Tech Computer Science", "MCA"],
    "description": "Lead cloud security architecture and automated compliance auditing.",
    "number_of_openings": 1
}

print("Testing job creation without deadline...")
try:
    res = requests.post(url, json=payload)
    print("Status:", res.status_code)
    if res.status_code in [200, 201]:
        print("Success! Created Job ID:", res.json().get("id"))
    else:
        print("Response:", res.text)
except Exception as e:
    print("Backend test error (server might be down/unreachable):", e)
