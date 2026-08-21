import os
import sys
from io import BytesIO

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.ai.banner_gen import create_job_banner

preview_dir = os.path.join(os.path.dirname(__file__), "generated_previews")
os.makedirs(preview_dir, exist_ok=True)

company_meta = {
    "background_color": "#F8F9FA",
    "website": "www.nexlogic.co.in",
    "apply_link": "https://egovtalent.com/jobs",
    "contact_email": "hr@naxlogic.com"
}

# 1. Single Job Test (Matching Exact Reference Banner: Project Manager Cyber Audit / SOC Manager)
single_job = [{
    "title": "PROJECT MANAGER – CYBER AUDIT – GRC SPECIALIST",
    "experience": "10+ Years",
    "number_of_openings": 2,
    "location": "Vijayawada / AP SOC Project",
    "work_mode": "100% On-site",
    "skills": ["CISA", "CISSP", "CISM", "ISO 27001", "GRC", "Cybersecurity", "Audit"]
}]

print("Generating Dense Single Job Banner...")
single_bytes = create_job_banner(single_job, company_meta)
single_path = os.path.join(preview_dir, "single_job.png")
with open(single_path, "wb") as f:
    f.write(single_bytes.getvalue())
print(f"Saved: {single_path} ({len(single_bytes.getvalue())} bytes)")

# 2. Multi-Job Test (Matching User Screenshot 2: Bengaluru / 3 Roles)
multi_jobs = [
    {
        "title": "UI/UX Designer",
        "experience": "2-5 Years",
        "number_of_openings": 2,
        "location": "Bengaluru, Karnataka",
        "skills": ["Figma", "Design Systems", "User Research", "Wireframing", "Prototyping"]
    },
    {
        "title": "Associate Software Engineer",
        "experience": "0-2 Years",
        "number_of_openings": 4,
        "location": "Bengaluru, Karnataka",
        "skills": ["JavaScript", "React.js", "Node.js", "SQL", "REST APIs", "Git"]
    },
    {
        "title": "Data Analyst",
        "experience": "1-3 Years",
        "number_of_openings": 2,
        "location": "Bengaluru, Karnataka",
        "skills": ["SQL", "Python", "Power BI", "Excel", "Data Modeling", "ETL"]
    }
]

print("Generating Dense Multi-Job Banner...")
multi_bytes = create_job_banner(multi_jobs, company_meta)
multi_path = os.path.join(preview_dir, "multi_job.png")
with open(multi_path, "wb") as f:
    f.write(multi_bytes.getvalue())
print(f"Saved: {multi_path} ({len(multi_bytes.getvalue())} bytes)")


