import sys
import os

try:
    from fastapi.testclient import TestClient
    from app.main import app
    from app.database.connection import get_db, Base, engine
    from app.models.schema import Job

    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    
    # Clean up old test jobs
    db.query(Job).delete()
    db.commit()

    print("--- TEST 1: REAL JOB ---")
    job1 = Job(title='Backend Dev', skills=['python', 'api'], location='New York', experience='3 years', company_id=1)
    db.add(job1)
    db.commit()

    client = TestClient(app)
    response = client.post(f'/candidates/search/{job1.id}')
    print("Status Code:", response.status_code)
    print("Response:", response.json())

    print("\n--- TEST 2: GARBAGE JOB (Router Filter) ---")
    job2 = Job(title='x', skills=['a'], location='', company_id=1)
    db.add(job2)
    db.commit()

    response = client.post(f'/candidates/search/{job2.id}')
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    
    print("\n--- TEST 3: LOW SCORE (Fails threshold) ---")
    # A job with many skills they probably won't have in their bio, so score will be low
    job3 = Job(title='Unicorn', skills=['rust', 'assembly', 'cobol', 'fortran'], location='San Francisco', company_id=1)
    db.add(job3)
    db.commit()

    response = client.post(f'/candidates/search/{job3.id}')
    print("Status Code:", response.status_code)
    print("Response:", response.json())

except Exception as e:
    import traceback
    traceback.print_exc()
