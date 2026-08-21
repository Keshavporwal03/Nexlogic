import os
import json
import time
import hashlib
import requests
from typing import List, Dict, Any

# Environment variables
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "public_search_cache.json")
CACHE_TTL = 86400  # 24 hours in seconds

STATE_CITY_MAP = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati", "Kurnool", "Rajahmundry", "Kakinada", "Anantapur", "Kadapa", "Eluru"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Roing", "Tezu"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Arrah", "Begusarai", "Katihar", "Munger"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Rajnandgaon", "Raigarh", "Jagdalpur", "Ambikapur"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Gandhinagar", "Anand", "Navsari", "Morbi", "Bharuch"],
    "Haryana": ["Faridabad", "Gurugram", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula"],
    "Himachal Pradesh": ["Shimla", "Dharamshala", "Mandi", "Solan", "Baddi", "Palampur", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh", "Giridih", "Ramgarh"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangaluru", "Belagavi", "Davangere", "Ballari", "Tumakuru", "Shivamogga", "Raichur", "Bidar", "Hospet", "Udupi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Palakkad", "Malappuram", "Kannur"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa", "Satna", "Ratlam", "Singrauli"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Amravati", "Navi Mumbai", "Kolhapur", "Akola", "Jalgaon", "Latur", "Dhule"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur"],
    "Meghalaya": ["Shillong", "Tura", "Nongstoin", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Brahmapur", "Sambalpur", "Puri", "Balasore", "Bhadrak"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Hoshiarpur", "Mohali", "Pathankot", "Moga"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur", "Bhilwara", "Alwar", "Sikar", "Pali", "Sri Ganganagar"],
    "Sikkim": ["Gangtok", "Namchi", "Mangan"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Tiruppur", "Salem", "Erode", "Tirunelveli", "Vellore", "Thoothukudi", "Dindigul", "Thanjavur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Mahbubnagar", "Nalgonda"],
    "Tripura": ["Agartala", "Dharmanagar", "Kailashahar", "Udaipur"],
    "Uttar Pradesh": ["Kanpur", "Lucknow", "Ghaziabad", "Agra", "Varanasi", "Meerut", "Prayagraj", "Bareilly", "Aligarh", "Moradabad", "Saharanpur", "Gorakhpur", "Noida", "Firozabad", "Jhansi", "Muzaffarnagar", "Mathura", "Ayodhya"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Kashipur", "Rishikesh"],
    "West Bengal": ["Kolkata", "Howrah", "Asansol", "Siliguri", "Durgapur", "Bardhaman", "Malda", "Baharampur", "Kharagpur", "Haldia"],
    "Delhi": ["New Delhi", "Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla"],
    "Ladakh": ["Leh", "Kargil"],
    "Chandigarh": ["Chandigarh"],
    "Puducherry": ["Pondicherry", "Ozhukarai", "Karaikal", "Yanam", "Mahe"],
    "Andaman and Nicobar Islands": ["Port Blair"]
}

NEIGHBORING_STATES_MAP = {
    "Andhra Pradesh": ["Telangana", "Odisha", "Tamil Nadu", "Karnataka"],
    "Arunachal Pradesh": ["Assam", "Nagaland"],
    "Assam": ["Arunachal Pradesh", "Nagaland", "Manipur", "Mizoram", "Tripura", "Meghalaya", "West Bengal"],
    "Bihar": ["Uttar Pradesh", "West Bengal", "Jharkhand"],
    "Chhattisgarh": ["Madhya Pradesh", "Maharashtra", "Telangana", "Andhra Pradesh", "Odisha", "Jharkhand", "Uttar Pradesh"],
    "Goa": ["Maharashtra", "Karnataka"],
    "Gujarat": ["Rajasthan", "Madhya Pradesh", "Maharashtra"],
    "Haryana": ["Punjab", "Himachal Pradesh", "Rajasthan", "Delhi", "Uttar Pradesh", "Uttarakhand", "Chandigarh"],
    "Himachal Pradesh": ["Jammu and Kashmir", "Ladakh", "Punjab", "Haryana", "Uttarakhand", "Uttar Pradesh"],
    "Jharkhand": ["Bihar", "West Bengal", "Odisha", "Chhattisgarh", "Uttar Pradesh"],
    "Karnataka": ["Goa", "Maharashtra", "Telangana", "Andhra Pradesh", "Tamil Nadu", "Kerala"],
    "Kerala": ["Karnataka", "Tamil Nadu", "Puducherry"],
    "Madhya Pradesh": ["Uttar Pradesh", "Chhattisgarh", "Maharashtra", "Gujarat", "Rajasthan"],
    "Maharashtra": ["Gujarat", "Madhya Pradesh", "Chhattisgarh", "Telangana", "Karnataka", "Goa"],
    "Manipur": ["Nagaland", "Mizoram", "Assam"],
    "Meghalaya": ["Assam"],
    "Mizoram": ["Tripura", "Assam", "Manipur"],
    "Nagaland": ["Arunachal Pradesh", "Assam", "Manipur"],
    "Odisha": ["West Bengal", "Jharkhand", "Chhattisgarh", "Andhra Pradesh"],
    "Punjab": ["Jammu and Kashmir", "Himachal Pradesh", "Haryana", "Rajasthan", "Chandigarh"],
    "Rajasthan": ["Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Gujarat"],
    "Sikkim": ["West Bengal"],
    "Tamil Nadu": ["Kerala", "Karnataka", "Andhra Pradesh", "Puducherry"],
    "Telangana": ["Maharashtra", "Chhattisgarh", "Karnataka", "Andhra Pradesh"],
    "Tripura": ["Assam", "Mizoram"],
    "Uttar Pradesh": ["Uttarakhand", "Himachal Pradesh", "Haryana", "Delhi", "Rajasthan", "Madhya Pradesh", "Chhattisgarh", "Jharkhand", "Bihar"],
    "Uttarakhand": ["Himachal Pradesh", "Uttar Pradesh", "Haryana"],
    "West Bengal": ["Odisha", "Jharkhand", "Bihar", "Sikkim", "Assam"],
    "Delhi": ["Haryana", "Uttar Pradesh"],
    "Jammu and Kashmir": ["Ladakh", "Himachal Pradesh", "Punjab"],
    "Ladakh": ["Jammu and Kashmir", "Himachal Pradesh"],
    "Chandigarh": ["Punjab", "Haryana"],
    "Puducherry": ["Tamil Nadu", "Andhra Pradesh", "Kerala"]
}

def get_fallback_cities(location: str) -> List[str]:
    if not location:
        return []
    loc_lower = location.lower()
    
    found_state = None
    for state, cities in STATE_CITY_MAP.items():
        if loc_lower in state.lower():
            found_state = state
            break
        for city in cities:
            if city.lower() in loc_lower or loc_lower in city.lower():
                found_state = state
                break
        if found_state:
            break
            
    if not found_state:
        return []
        
    fallback_cities = list(STATE_CITY_MAP[found_state])
    
    # Append neighboring states' cities at the end of the fallback list
    if found_state in NEIGHBORING_STATES_MAP:
        for neighbor in NEIGHBORING_STATES_MAP[found_state]:
            if neighbor in STATE_CITY_MAP:
                fallback_cities.extend(STATE_CITY_MAP[neighbor])
                
    return fallback_cities

def _get_cache() -> Dict[str, Any]:
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Cache load error: {e}")
    return {}

def _save_cache(cache_data: Dict[str, Any]) -> None:
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Cache save error: {e}")

def search_candidates(job_title: str, required_skills: List[str], location: str, experience: str = "", education: List[str] = None, description: str = "") -> Dict[str, Any]:
    """
    Orchestrates candidate search across LinkedIn, GitHub, and Serper.dev (Public LinkedIn Search).
    Includes location fallback logic and passes experience/education for better matching.
    """
    candidates = []
    quota_exhausted = False
    
    locations_to_try = [location] if location else [""]
    
    # State-level fallback logic mapped to location
    fallback_cities = get_fallback_cities(location)
    for city in fallback_cities:
        if city.lower() not in (location or "").lower():
            locations_to_try.append(city)

    seen_urls = set()

    for loc in locations_to_try:
        if len(candidates) >= 10:
            break
            
        print(f"[*] Searching for candidates in location: {loc or 'Any'}")
        
        # Priority 1: LinkedIn API
        if LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET and LINKEDIN_ACCESS_TOKEN:
            try:
                li_candidates = search_linkedin(job_title, required_skills, loc, experience, education, description)
                for c in li_candidates:
                    if c.get("profile_url") not in seen_urls:
                        candidates.append(c)
                        seen_urls.add(c.get("profile_url"))
            except Exception as e:
                print(f"LinkedIn search failed: {e}. Falling back to secondary sources.")

        if len(candidates) >= 10: break

        # Priority 2: GitHub API
        try:
            gh_candidates = search_github(job_title, required_skills, loc, experience, education, description)
            for c in gh_candidates:
                if c.get("profile_url") not in seen_urls:
                    candidates.append(c)
                    seen_urls.add(c.get("profile_url"))
        except Exception as e:
            print(f"GitHub search failed: {e}")
            
        if len(candidates) >= 10: break

        # Priority 3: Serper.dev Public Search
        try:
            serper_res = search_serper_dev(job_title, required_skills, loc, experience, education, description)
            serper_candidates = serper_res.get("candidates", [])
            if serper_res.get("quota_exhausted", False):
                quota_exhausted = True
            for c in serper_candidates:
                if c.get("profile_url") not in seen_urls:
                    candidates.append(c)
                    seen_urls.add(c.get("profile_url"))
        except Exception as e:
            print(f"Serper.dev Search failed: {e}")

    return {"candidates": candidates, "quota_exhausted": quota_exhausted}

def search_linkedin(job_title: str, skills: List[str], location: str, experience: str = "", education: List[str] = None, description: str = "") -> List[Dict]:
    """
    Placeholder for official LinkedIn Talent API search.
    """
    print("Executing LinkedIn Search API (Stub)...")
    return []

def search_github(job_title: str, skills: List[str], location: str, experience: str = "", education: List[str] = None, description: str = "") -> List[Dict]:
    """
    Searches GitHub for users matching the given skills and location.
    """
    candidates = []
    
    search_terms = skills.copy() if skills else []
    if not search_terms and description:
        desc_words = [w for w in description.replace(",", " ").split() if len(w) > 4]
        search_terms = desc_words[:3]
    if not search_terms and job_title:
        title_words = [w for w in job_title.replace("-", " ").split() if len(w) > 3]
        search_terms = title_words[:2]
        
    if not search_terms:
        return candidates

    query_parts = []
    for term in search_terms[:3]:
        if " " in term:
            query_parts.append(f'"{term}"')
        else:
            query_parts.append(term)
        
    if location:
        query_parts.append(f'location:"{location}"')
        
    query = " ".join(query_parts)
    url = "https://api.github.com/search/users"
    params = {"q": query, "per_page": 10}
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_API_TOKEN:
        headers["Authorization"] = f"token {GITHUB_API_TOKEN}"
        
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", [])[:5]:
            user_res = requests.get(item.get("url"), headers=headers)
            if user_res.status_code == 200:
                user_data = user_res.json()
                user_loc = user_data.get("location") or ""
                user_bio = user_data.get("bio") or ""
                
                score = 0.0
                matched_skills = []
                for s in search_terms:
                    if s.lower() in user_bio.lower():
                        matched_skills.append(s)
                
                # Skills Match (40 pts max)
                if search_terms:
                    score += (len(matched_skills) / len(search_terms)) * 40.0
                else:
                    score += 40.0
                    
                # Location Match (20 pts max)
                if location and (location.lower() in user_loc.lower() or user_loc.lower() in location.lower()):
                    score += 20.0
                else:
                    score += 10.0
                    
                # Experience Match (20 pts max)
                if experience and (str(experience).lower() in user_bio.lower() or "senior" in user_bio.lower() or "lead" in user_bio.lower()):
                    score += 20.0
                else:
                    score += 10.0
                    
                # Education Match (10 pts max)
                if education:
                    if any(e.lower() in user_bio.lower() for e in education):
                        score += 10.0
                    else:
                        score += 5.0
                else:
                    score += 10.0

                final_score = round(min(95.0, max(60.0, score + 10.0)), 1)

                candidates.append({
                    "name": user_data.get("name") or item.get("login"),
                    "profile_url": item.get("html_url"),
                    "source": "GitHub",
                    "skills": matched_skills if matched_skills else (search_terms[:1] if search_terms else []),
                    "location": user_loc,
                    "match_score": final_score,
                    "unverified": False
                })
    return candidates

def _parse_candidate_name(title: str) -> str:
    if not title: return "Unknown Candidate"
    clean = title.replace(" - LinkedIn", "").replace(" | LinkedIn", "")
    parts = clean.split(" - ")
    if not parts or len(parts[0]) == len(clean):
        parts = clean.split(" | ")
    candidate_name = parts[0].strip()
    if not candidate_name or candidate_name.lower() == "linkedin":
        return "LinkedIn Profile"
    return candidate_name

def search_serper_dev(job_title: str, required_skills: List[str], location: str, experience: str = "", education: List[str] = None, description: str = "") -> Dict[str, Any]:
    if not SERPER_API_KEY:
        print("[Serper.dev] API Key missing. Skipping.")
        return {"candidates": [], "quota_exhausted": False}

    search_terms = required_skills.copy() if required_skills else []
    if not search_terms and description:
        desc_words = [w for w in description.replace(",", " ").split() if len(w) > 4]
        search_terms = desc_words[:2]

    skills_key = ",".join(sorted([s.strip().lower() for s in (search_terms or [])]))
    query_raw = f"{job_title.strip().lower()}:{skills_key}:{location.strip().lower()}"
    cache_key = hashlib.sha256(query_raw.encode("utf-8")).hexdigest()

    cache = _get_cache()
    cached_entry = cache.get(cache_key)
    now = time.time()

    if cached_entry and (now - cached_entry.get("timestamp", 0) < CACHE_TTL):
        return cached_entry.get("data", {"candidates": [], "quota_exhausted": False})

    query_parts = ["site:linkedin.com/in"]
    clean_title = job_title.split("/")[0].strip() if job_title else ""
    if clean_title:
        query_parts.append(f'"{clean_title}"')

    short_skills = []
    for s in (search_terms or []):
        s_clean = s.strip()
        if len(s_clean) <= 25 and "(" not in s_clean and ")" not in s_clean:
            short_skills.append(s_clean)
        if len(short_skills) >= 2: break
            
    for s in short_skills:
        query_parts.append(f'"{s}"' if " " in s else s)
        
    if location:
        clean_loc = location.split(",")[0].split("/")[0].strip()
        if clean_loc:
            query_parts.append(f'"{clean_loc}"' if " " in clean_loc else clean_loc)

    search_query = " ".join(query_parts)
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = json.dumps({"q": search_query})

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        
        if response.status_code in [401, 403, 429]:
            return {"candidates": [], "quota_exhausted": True}
        if response.status_code != 200:
            return {"candidates": [], "quota_exhausted": False}

        data = response.json()
        if "message" in data:
            msg = str(data["message"]).lower()
            is_quota = any(term in msg for term in ["unauthorized", "quota", "credit", "not enough credits", "limit"])
            return {"candidates": [], "quota_exhausted": is_quota}

        items = data.get("organic", [])
        
        if len(items) == 0 and clean_title:
            fallback_query_parts = ["site:linkedin.com/in", f'"{clean_title}"']
            if location:
                clean_loc = location.split(",")[0].split("/")[0].strip()
                if clean_loc:
                    fallback_query_parts.append(f'"{clean_loc}"' if " " in clean_loc else clean_loc)
            
            fb_payload = json.dumps({"q": " ".join(fallback_query_parts)})
            try:
                fb_resp = requests.post(url, headers=headers, data=fb_payload, timeout=10)
                if fb_resp.status_code == 200:
                    items = fb_resp.json().get("organic", [])
            except:
                pass

        candidates = []
        for item in items:
            link = item.get("link", "")
            if "linkedin.com/in/" not in link: continue

            raw_title = item.get("title", "")
            snippet = item.get("snippet", "")
            combined_text = f"{raw_title} {snippet}".lower()
            candidate_name = _parse_candidate_name(raw_title)

            score = 0.0
            
            # Experience Match (30 pts)
            if experience and (str(experience).lower() in combined_text or "senior" in combined_text or "experienced" in combined_text):
                score += 30.0
            else:
                score += 15.0

            # Job Title/Role Relevance (25 pts)
            job_title_lower = clean_title.lower() if clean_title else ""
            if job_title_lower and (job_title_lower in combined_text or any(t in combined_text for t in job_title_lower.split() if len(t)>2)):
                score += 25.0
            else:
                score += 10.0

            # Skills Match (25 pts)
            matched_skills = []
            for s in (search_terms or []):
                if s.lower() in combined_text:
                    matched_skills.append(s)
            if search_terms:
                score += min(25.0, max(10.0, (len(matched_skills) / len(search_terms)) * 25.0))
            else:
                score += 20.0
                
            # Education Match (10 pts)
            if education:
                if any(e.lower() in combined_text for e in education):
                    score += 10.0
                else:
                    score += 5.0
            else:
                score += 10.0

            # Location Match (10 pts)
            clean_loc = location.split(",")[0].split("/")[0].strip().lower() if location else ""
            if clean_loc and clean_loc in combined_text:
                score += 10.0
            else:
                score += 5.0

            final_match_score = round(min(95.0, max(60.0, score)), 1)

            candidates.append({
                "name": candidate_name,
                "profile_url": link,
                "source": "Serper.dev (Public LinkedIn)",
                "skills": matched_skills if matched_skills else (search_terms[:1] if search_terms else []),
                "location": location if (location and clean_loc and clean_loc in combined_text) else "",
                "match_score": final_match_score,
                "unverified": True,
                "unverified_snippet": snippet[:200]
            })

        res_data = {"candidates": candidates, "quota_exhausted": False}
        if candidates:
            cache[cache_key] = {"timestamp": now, "data": res_data}
            _save_cache(cache)

        return res_data

    except Exception as e:
        print(f"[Serper.dev] REQUEST EXCEPTION: {e}")
        return {"candidates": [], "quota_exhausted": False}
