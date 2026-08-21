import sys
import os

try:
    from app.services.search import search_candidates
    job_title = 'Backend Engineer'
    required_skills = ['Java', 'Spring Boot', 'AWS']
    location = 'New York'

    print('Calling search_candidates...')
    results = search_candidates(job_title, required_skills, location)
    print('Results returned:', len(results))
    
    saved_candidates = []
    for res in results:
        score = res.get('match_score', 0.0)
        print(f"DEBUG: Candidate {res.get('name')} computed score before threshold: {score}")
        if score < 30.0:
            continue
        saved_candidates.append(res)
    print('Final candidates count:', len(saved_candidates))
except Exception as e:
    import traceback
    traceback.print_exc()
