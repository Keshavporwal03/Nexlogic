import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.models.schema import Company, Job

db = SessionLocal()
company = db.query(Company).first()

if company:
    print("--- COMPANY TABLE IN DB ---")
    print(f"ID: {company.id}")
    print(f"Website: '{company.website}'")
    print(f"Apply Link: '{company.apply_link}'")
    print(f"Contact Email: '{company.contact_email}'")

else:
    print("No company record found in DB.")

print("\n--- RECENT JOBS IN DB & THEIR APPLY_LINK ---")
jobs = db.query(Job).order_by(Job.id.desc()).limit(10).all()
for j in jobs:
    print(f"Job ID {j.id}: Title='{j.title}' | Apply Link='{j.apply_link}' | Deadline='{j.deadline}'")

db.close()
