import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.database.connection import SessionLocal
from app.models.schema import Job

def delete_legacy_jobs():
    db = SessionLocal()
    try:
        legacy_jobs = db.query(Job).filter(
            (Job.experience == None) | 
            (Job.remote_type == None) | 
            (Job.description == None) | 
            (Job.deadline == None)
        ).all()
        
        count = len(legacy_jobs)
        for job in legacy_jobs:
            db.delete(job)
        
        db.commit()
        print(f"Deleted {count} legacy jobs.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    delete_legacy_jobs()
