from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

import os
import time
import uuid
from supabase import create_client, Client

from app.ai.banner_gen import create_job_banner
from app.ai.post_gen import generate_linkedin_post
from app.ai.job_extractor import extract_job_details
from app.database.connection import get_db
from app.models.schema import Company, Banner

router = APIRouter(prefix="/ai", tags=["AI Generation"])


class BannerRequest(BaseModel):
    job_details: Optional[Dict[str, Any]] = None
    jobs: Optional[List[Dict[str, Any]]] = None
    company_colors: Optional[Dict[str, Any]] = None


class PostRequest(BaseModel):
    job_details: Optional[Dict[str, Any]] = None
    jobs: Optional[List[Dict[str, Any]]] = None


class ExtractRequest(BaseModel):
    text: str


@router.post("/extract-job")
def extract_job(req: ExtractRequest):
    data = extract_job_details(req.text)
    return data


@router.post("/banner")
def generate_banner(req: BannerRequest, db: Session = Depends(get_db)):
    company = db.query(Company).first()
    
    # Support both single job and multi-job payloads
    target_jobs = req.jobs if req.jobs else ([req.job_details] if req.job_details else [])
    colors = req.company_colors.copy() if req.company_colors else {}
    
    job_apply_link = None
    if target_jobs and len(target_jobs) > 0 and target_jobs[0]:
        job_apply_link = target_jobs[0].get("apply_link")

    active_apply_link = colors.get("apply_link") or job_apply_link or (company.apply_link if company else None) or "https://egovtalent.com/"
    colors["apply_link"] = active_apply_link

    if company:
        colors["website"] = colors.get("website") or (company.website if company.website and "nexlogic" not in company.website else active_apply_link)
        colors["primary_color"] = colors.get("primary_color") or company.primary_color or "#384F3E"
        if "why_join_us" not in colors or not colors["why_join_us"]:
            colors["why_join_us"] = company.why_join_us or []
            
    # Returns a BytesIO object
    image_bytes = create_job_banner(target_jobs, colors)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        try:
            supabase: Client = create_client(supabase_url, supabase_key)
            file_name = f"banner_{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
            
            image_bytes.seek(0)
            supabase.storage.from_("banners").upload(
                file=image_bytes.read(),
                path=file_name,
                file_options={"content-type": "image/png"}
            )
            image_bytes.seek(0)
            
            public_url = supabase.storage.from_("banners").get_public_url(file_name)
            
            job_id = None
            if target_jobs and len(target_jobs) > 0 and target_jobs[0]:
                job_id = target_jobs[0].get("id")
                
            if job_id:
                banner = Banner(job_id=job_id, image_url=public_url)
                db.add(banner)
                db.commit()
        except Exception as e:
            print(f"Failed to upload banner to Supabase: {e}")
            image_bytes.seek(0)

    return StreamingResponse(image_bytes, media_type="image/png")



@router.post("/post")
def generate_post(req: PostRequest, db: Session = Depends(get_db)):
    company = db.query(Company).first()
    
    target_jobs = req.jobs if req.jobs else ([req.job_details] if req.job_details else [])
    
    for job in target_jobs:
        if company:
            if "company_details" not in job:
                job["company_details"] = {}
                
            job["company_details"]["why_join_us"] = company.why_join_us or []
            job["company_details"]["contact_email"] = company.contact_email
            job["company_details"]["apply_link"] = job.get("apply_link") or company.apply_link
        
    post_text = generate_linkedin_post(target_jobs)
    return {"post": post_text}
