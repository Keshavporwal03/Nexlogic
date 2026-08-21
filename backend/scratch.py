import os
import sys
from app.ai.banner_gen import create_job_banner

if __name__ == "__main__":
    jobs_single = [{
        "title": "Software Engineer", 
        "experience": "3+ Years", 
        "location": "Remote", 
        "description": "Build cool things.",
        "number_of_openings": 1,
        "apply_link": "https://careers.egovtalent.com/apply/cloud-eng-101"

    }]
    jobs_multi = [
        {
            "title": "DATA CENTRE CYBERSECURITY LEAD", 
            "location": "NOT SPECIFIED IN THE TEXT, LIKELY A SPECIFIC DATA CENTRE LOCATION", 
            "experience": "8-12 years", 
            "number_of_openings": 1,
            "skills": ["CSOC coordination", "cybersecurity monitoring", "security event analysis", "incident triage and investigation"]
        }, 
        {
            "title": "NETWORK SECURITY & INFRASTRUCTURE", 
            "location": "NOT SPECIFIED IN THE TEXT, LIKELY A SPECIFIC DATA CENTRE LOCATION", 
            "experience": "7-10 years", 
            "number_of_openings": 1,
            "skills": ["Administering and monitoring Data Centre network security infrastructure", "Working with Routers", "Core/distribution switches", "Firewalls"]
        },
        {
            "title": "VULNERABILITY, PATCH & SECURITY", 
            "location": "NOT SPECIFIED IN THE TEXT, LIKELY A SPECIFIC DATA CENTRE LOCATION", 
            "experience": "6-10 years", 
            "number_of_openings": 1,
            "skills": ["Data Centre patch management framework development", "Inventory maintenance", "OS and security patch deployment coordination", "Critical and high-risk vulnerability tracking"]
        }
    ]
    colors = {
        "primary_color": "#0C4A2B", 
        "background_color": "#FAF7F3", 
        "apply_link": "https://egovtalent.com/", 
        "website": "www.eGovTalent.com",
        "contact_email": "hr@naxlogic.com",
        "why_join_us": ["Competitive Salary", "Remote Work", "Health Insurance"]
    }

    
    artifact_dir = os.path.join(os.path.dirname(__file__), "generated_previews")
    os.makedirs(artifact_dir, exist_ok=True)

    
    with open(os.path.join(artifact_dir, "single_test.png"), "wb") as f:
        f.write(create_job_banner(jobs_single, colors).read())
    with open(os.path.join(artifact_dir, "multi_test.png"), "wb") as f:
        f.write(create_job_banner(jobs_multi, colors).read())
    print("Done generating tests")
