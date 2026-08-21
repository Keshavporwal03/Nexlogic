import sys
import os

try:
    from app.services.search import search_candidates

    print("--- SCENARIO 3: UNRELATED SEARCH (Low Score Filter) ---")
    res3 = search_candidates('Developer', ['graphql', 'rust', 'svelte'], 'San Francisco')
    
    saved_candidates = []
    for res in res3:
        score = res.get("match_score", 0.0)
        print(f"DEBUG: Candidate {res.get('name')} computed score before threshold: {score}")
        if score < 30.0:
            continue
        saved_candidates.append(res)
        
    print("Candidates passed filter:", len(saved_candidates))

except Exception as e:
    import traceback
    traceback.print_exc()
