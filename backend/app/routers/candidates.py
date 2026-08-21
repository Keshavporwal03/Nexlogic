from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
from io import StringIO
from app.database.connection import get_db
from app.models.schema import Candidate, Job
from app.services.search import search_candidates

router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/search/{job_id}")
def run_candidate_search(job_id: int, db: Session = Depends(get_db)):
    """
    Triggers an automated search (LinkedIn -> GitHub) based on the job's requirements.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"error": "Job not found"}
        
    # Basic input validation to prevent garbage searches
    import re
    def is_garbage(text):
        if not text: return True
        if len(text) < 2: return True
        # If it doesn't contain at least one vowel, it's likely garbage keysmash
        if not re.search(r'[aeiouyAEIOUY]', text): return True
        return False

    if is_garbage(job.title) or (job.skills and all(is_garbage(s) for s in job.skills)):
        return {"message": "No candidates found", "candidates": []}
        
    search_res = search_candidates(
        job_title=job.title,
        required_skills=job.skills,
        location=job.location,
        experience=job.experience,
        education=job.education_requirements,
        description=job.description
    )
    if isinstance(search_res, dict):
        results = search_res.get("candidates", [])
        quota_exhausted = search_res.get("quota_exhausted", False)
    else:
        results = search_res or []
        quota_exhausted = False
    
    # Save results to db and filter by threshold
    saved_candidates = []
    threshold = job.match_threshold if job.match_threshold is not None else 30.0

    for res in results:
        score = res.get("match_score", 0.0)
        is_unverified = res.get("unverified", False) or "Serper" in (res.get("source") or "") or "Google" in (res.get("source") or "")
        print(f"DEBUG: Candidate {res.get('name')} (source={res.get('source')}) score={score}, threshold={threshold}, unverified={is_unverified}")

        # Filter out low/no-match results ONLY for verified sources (GitHub/LinkedIn).
        # Unverified public web search candidates bypass threshold filtering for manual review.
        if not is_unverified and score < threshold:
            continue
            
        candidate = Candidate(
            job_id=job.id,
            name=res.get("name"),
            skills=res.get("skills", []),
            location=res.get("location", ""),
            source=res.get("source"),
            profile_url=res.get("profile_url"),
            match_score=score
        )
        db.add(candidate)
        saved_candidates.append(candidate)
        
    db.commit()
    
    filtered_candidates = [
        c for c in results 
        if (c.get("unverified", False) or "Serper" in (c.get("source") or "") or "Google" in (c.get("source") or "") or c.get("match_score", 0.0) >= threshold)
    ]

    message = f"Found {len(filtered_candidates)} candidates via API."
    if quota_exhausted:
        message += " Note: Serper.dev public search query allowance is exhausted."

    return {
        "message": message,
        "candidates": filtered_candidates,
        "quota_exhausted": quota_exhausted,
        "quota_warning": "Serper.dev public search query allowance is exhausted (2,500 free query limit reached). Showing results from available fallback sources." if quota_exhausted else None
    }




@router.post("/upload/{job_id}")
def upload_candidates_csv(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload candidates via CSV. Useful for non-developer roles.
    Expected CSV columns: name, skills (comma separated), experience, location, profile_url
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"error": "Job not found"}

    content = file.file.read().decode("utf-8")
    csv_reader = csv.DictReader(StringIO(content))
    
    count = 0
    for row in csv_reader:
        skills = [s.strip() for s in row.get("skills", "").split(",")] if row.get("skills") else []
        
        # Strict Match Scoring: Skills 40% / Experience 30% / Location 20% / Education 10%
        score = 0.0
        
        # Skills (40%)
        job_skills = set(job.skills) if job.skills else set()
        if job_skills:
            matched = set(skills).intersection(job_skills)
            score += (len(matched) / len(job_skills)) * 40.0
        else:
            score += 40.0 # Full points if no skills required
            
        # Experience (30%) - String match approximation
        candidate_exp = row.get("experience", "")
        job_exp = job.experience or ""
        if not job_exp or str(job_exp).lower() in str(candidate_exp).lower():
            score += 30.0
            
        # Location (20%) - String match approximation
        candidate_loc = row.get("location", "")
        job_loc = job.location or ""
        if not job_loc or str(job_loc).lower() in str(candidate_loc).lower():
            score += 20.0
            
        # Education (10%) - Defaulting to 0 since not present in CSV for now, 
        # or checking an arbitrary education column if added later.
        candidate_edu = row.get("education", "")
        if candidate_edu:
            score += 10.0

        candidate = Candidate(
            job_id=job.id,
            name=row.get("name", "Unknown"),
            skills=skills,
            experience=row.get("experience", "Unknown"),
            location=row.get("location", ""),
            source="CSV Upload",
            profile_url=row.get("profile_url", ""),
            match_score=score
        )
        db.add(candidate)
        count += 1
        
    db.commit()
    return {"message": f"Successfully imported {count} candidates."}
