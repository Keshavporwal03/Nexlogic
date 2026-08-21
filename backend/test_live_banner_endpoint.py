import requests

url = "http://127.0.0.1:8000/ai/banner"

payload = {
    "jobs": [
        {
            "title": "Lead DevOps & Cloud Engineer",
            "location": "Noida",
            "experience": "5+ Years",
            "apply_link": "https://mycustomcompany.com/apply/job-55",
            "skills": ["Kubernetes", "AWS", "Terraform", "Docker"]
        }
    ]
}

print("Testing live /ai/banner endpoint with custom apply_link...")
res = requests.post(url, json=payload)
print("HTTP Status:", res.status_code)

if res.status_code == 200:
    with open("f:/Recruitment-AI/backend/generated_previews/live_endpoint_test.png", "wb") as f:
        f.write(res.content)
    print("Saved live endpoint banner image!")
else:
    print("Error:", res.text)
