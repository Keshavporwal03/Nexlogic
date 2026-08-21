from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.database.connection import get_db
from app.models.schema import Company

router = APIRouter(prefix="/company", tags=["Company"])


class CompanyProfileBase(BaseModel):
    apply_link: Optional[str] = None
    contact_email: Optional[str] = None
    why_join_us: Optional[List[str]] = []
    primary_color: Optional[str] = None


@router.get("/profile", response_model=CompanyProfileBase)
def get_company_profile(db: Session = Depends(get_db)):
    """
    Returns the default company profile (the first one).
    Creates a dummy one if it doesn't exist for V1 purposes.
    """
    company = db.query(Company).first()
    if not company:
        # Create a default company record if none exists
        company = Company(
            company_name="Default Company",
            apply_link="",
            contact_email="",
            why_join_us=["Great culture", "Competitive salary"],
            primary_color="#384F3E" # Dark Olive Green
        )
        db.add(company)
        db.commit()
        db.refresh(company)

    return {
        "apply_link": company.apply_link,
        "contact_email": company.contact_email,
        "why_join_us": company.why_join_us or [],
        "primary_color": company.primary_color,
    }


@router.post("/profile")
def update_company_profile(
    profile: CompanyProfileBase, db: Session = Depends(get_db)
):
    """
    Updates the default company profile.
    """
    company = db.query(Company).first()
    if not company:
        company = Company(company_name="Default Company")
        db.add(company)

    company.apply_link = profile.apply_link
    company.contact_email = profile.contact_email
    company.why_join_us = profile.why_join_us
    if profile.primary_color:
        company.primary_color = profile.primary_color

    db.commit()
    return {"message": "Company profile updated successfully"}
