import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.models.schema import Company

db = SessionLocal()
company = db.query(Company).first()

if company:
    company.website = "https://egovtalent.com/"
    company.apply_link = "https://egovtalent.com/"
    db.commit()
    print("Successfully updated Company record in DB!")
    print(f"Company ID {company.id}: Website='{company.website}', ApplyLink='{company.apply_link}'")
else:
    print("No Company record in DB.")

db.close()
