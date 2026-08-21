import os
import requests

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://router.huggingface.co/v1/chat/completions"

def generate_linkedin_post(jobs: list) -> str:
    """
    Generates a LinkedIn hiring post using Hugging Face text models.
    """
    if not HF_API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY is not set.")

    if not jobs:
        return ""

    if len(jobs) == 1:
        job_details = jobs[0]
        title = job_details.get("title", "an open role")
        company = job_details.get("company_name", "our company")
        location = job_details.get("location", "various locations")
        position_details = [
            f"- Job Title: {title}",
            f"- Location: {location}"
        ]
        if job_details.get("experience"):
            position_details.append(f"- Experience: {job_details.get('experience')}")
        if job_details.get("education"):
            position_details.append(f"- Education: {job_details.get('education')}")
        if job_details.get("skills"):
            position_details.append(f"- Skills: {', '.join(job_details.get('skills'))}")
        if job_details.get("certificates"):
            position_details.append(f"- Certificates: {job_details.get('certificates')}")
            
        position_details_str = "\n           ".join(position_details)
        
        job_profile_parts = []
        if job_details.get("description"):
            job_profile_parts.append(f"Description: {job_details.get('description')}")
        if job_details.get("role_objective"):
            job_profile_parts.append(f"Role Objective: {job_details.get('role_objective')}")
        if job_details.get("key_responsibilities"):
            job_profile_parts.append(f"Key Responsibilities: {job_details.get('key_responsibilities')}")
            
        job_profile_str = "\n           ".join(job_profile_parts)
        if not job_profile_str:
            job_profile_str = "Join our amazing team."
        
        company_details = job_details.get("company_details", {})
        why_join_us = company_details.get("why_join_us", ["Great culture", "Competitive salary"])
        why_join_us_str = "\\n".join([f"- {bullet}" for bullet in why_join_us])
        
        apply_link = job_details.get("apply_link") or company_details.get("apply_link", "Link not provided")
        contact_email = company_details.get("contact_email", "Email not provided")
        
        prompt = f'''
        Write a professional and engaging LinkedIn post announcing that {company} is hiring for the position of {title}.
        
        Structure the post EXACTLY as follows (DO NOT include fields that are missing below):
        1. A short energetic hook/intro line for the role. (Include emojis like 🚀 📢 💼 📍 🎯).
        2. Position Details:
           {position_details_str}
        3. Job Profile: (Summarize the following details briefly)
           {job_profile_str}
        4. Why Join Us:
        {why_join_us_str}
        5. Apply Now: {apply_link}
           Email: {contact_email}
        6. Know someone who's a great fit? Tag them in the comments!
        7. A rich, relevant hashtag set based on: role, skills, location, industry, and generic hiring.

        Do not output any introductory or concluding text outside of this exact structure. Do not hallucinate or add any random skills, education, or requirements if they are not explicitly provided.
        '''
    else:
        # Multi-job logic
        company = jobs[0].get("company_name", "our company")
        company_details = jobs[0].get("company_details", {})
        why_join_us = company_details.get("why_join_us", ["Great culture", "Competitive salary"])
        why_join_us_str = "\\n".join([f"- {bullet}" for bullet in why_join_us])
        apply_link = company_details.get("apply_link", "Link not provided")
        contact_email = company_details.get("contact_email", "Email not provided")

        locations = {}
        for job in jobs:
            loc = job.get('location') or 'Multiple Locations'
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(job)

        jobs_str = ""
        for loc, loc_jobs in locations.items():
            jobs_str += f"📍 {loc}\\n"
            for job in loc_jobs:
                jobs_str += f"- {job.get('title')} ({job.get('experience', 'Exp not specified')})\\n"
            jobs_str += "\\n"

        prompt = f'''
        Write a professional and engaging LinkedIn post announcing that {company} is hiring across multiple locations.
        
        Structure the post EXACTLY as follows:
        1. A short energetic hook/intro line for hiring across multiple locations. (Include emojis like 🚀 📢 💼 📍 🎯).
        2. A brief company introduction.
        3. Open Positions (Grouped by location):
        {jobs_str}
        4. Why Join Us:
        {why_join_us_str}
        5. Apply Now: {apply_link}
           Email: {contact_email}
        6. Know someone who's a great fit? Tag them in the comments!
        7. A rich, relevant hashtag set based on: locations, roles, industry, and generic hiring.

        Do not output any introductory or concluding text outside of this exact structure.
        '''

    prompt += f'''
    Below are two style/structure references for how the final post should look. Do not copy these verbatim; generate fresh content for the real job data using these as a structural guide.

    STYLE REFERENCE 1 (SINGLE-JOB):
    ---
    🚀🎯 We're Hiring a Senior Software Engineer to help build the future of secure government tech!

    **Position Details:**
    - Job Title: Senior Software Engineer
    - Location: Noida
    - Experience: 5+ Years

    **Job Profile:** Design, build, and maintain scalable web applications, collaborate with cross-functional teams, and mentor junior developers.

    **Why Join Us:**
    - Work on prestigious Government projects
    - Competitive compensation & growth opportunities
    - Collaborate with industry experts
    - Immediate joiners preferred

    **Apply Now:** https://egovtalent.com/
    Email: hr@nexlogictalent.com

    Know someone who's a great fit? Tag them in the comments or share this post with your network.

    #Hiring #SoftwareEngineer #Noida #TechJobs #GovernmentProjects #CareerOpportunity #NexLogic #eGovTalent
    ---

    STYLE REFERENCE 2 (MULTI-JOB, GROUPED BY LOCATION):
    ---
    🚀 We're Hiring Across Multiple Locations | Join High-Impact Government Digital Transformation Projects

    NexLogic, through eGovTalent, is hiring experienced professionals for prestigious e-Governance and Information Security projects.

    **Open Positions**

    📍 Manipur — Government Information Security (ISMS) Project
    - Project Manager (PM)
    - Senior Consultant (ISMS Lead)

    📍 Lucknow — Government Consulting Project
    - Team Leader / Lead Transaction Advisor
    - Procurement Expert

    **Why Join Us:**
    - Work on prestigious Government projects
    - Competitive compensation & growth opportunities
    - Immediate joiners preferred

    **Apply Now:** https://egovtalent.com/
    Email: hr@nexlogictalent.com

    Know someone who's a great fit? Tag them in the comments or share this post with your network.

    #Hiring #GovernmentJobs #eGovernance #DigitalIndia #ManipurJobs #LucknowJobs #NexLogic #eGovTalent
    ---
    '''

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 250,
        "temperature": 0.7,
        "stream": False
    }


    # Attempt up to 2 times
    for attempt in range(2):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                generated_text = result["choices"][0].get("message", {}).get("content", "").strip()
                
                # Check for profanity
                if not profanity.contains_profanity(generated_text):
                    return generated_text
                else:
                    print(f"Warning: Profanity detected in generated text (Attempt {attempt + 1}).")
            else:
                print(f"Failed to parse generation result (Attempt {attempt + 1}).")
        except requests.exceptions.RequestException as e:
            if getattr(e, 'response', None) is not None:
                print(f"HTTP Error (Attempt {attempt + 1}): {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            else:
                print(f"Request Error (Attempt {attempt + 1}): {e}")
        except Exception as e:
            print(f"Error generating text (Attempt {attempt + 1}): {e}")
            
    # If we exhaust 2 attempts and it's still failing/flagged, fallback to neutral template
    print("Falling back to neutral template after 2 failed/flagged attempts.")
    return generate_fallback_post(jobs)

from better_profanity import profanity

def filter_profanity(text: str) -> str:
    """
    Basic profanity filter using better-profanity.
    If the text contains profanity, it censors it or you can choose to reject.
    For this use case, we censor and return.
    """
    if profanity.contains_profanity(text):
        print("Warning: Profanity detected in generated text.")
        return profanity.censor(text)
    return text.strip()

def generate_fallback_post(jobs: list) -> str:
    """
    Fallback neutral template if AI generation fails or is flagged.
    """
    if not jobs:
        return ""
        
    if len(jobs) == 1:
        job_details = jobs[0]
        title = job_details.get("title", "an open position")
        company = job_details.get("company_name", "our team")
        location = job_details.get("location", "various locations")
        position_details = [
            f"• Job Title: {title}",
            f"• Location: {location}"
        ]
        if job_details.get("experience"):
            position_details.append(f"• Experience: {job_details.get('experience')}")
        if job_details.get("education"):
            position_details.append(f"• Education: {job_details.get('education')}")
        if job_details.get("skills"):
            position_details.append(f"• Skills: {', '.join(job_details.get('skills'))}")
        if job_details.get("certificates"):
            position_details.append(f"• Certificates: {job_details.get('certificates')}")
            
        position_details_str = "\n".join(position_details)
        
        job_profile_parts = []
        if job_details.get("description"):
            job_profile_parts.append(f"Description: {job_details.get('description')}")
        if job_details.get("role_objective"):
            job_profile_parts.append(f"Role Objective: {job_details.get('role_objective')}")
        if job_details.get("key_responsibilities"):
            job_profile_parts.append(f"Key Responsibilities:\n{job_details.get('key_responsibilities')}")
            
        job_profile_str = "\n\n".join(job_profile_parts)
        if not job_profile_str:
            job_profile_str = "Join our amazing team."
        
        company_details = job_details.get("company_details", {})
        why_join_us = company_details.get("why_join_us", ["Great culture", "Competitive salary"])
        why_join_us_str = "\\n".join([f"✨ {bullet}" for bullet in why_join_us])
        
        apply_link = job_details.get("apply_link") or company_details.get("apply_link", "Link not provided")
        contact_email = company_details.get("contact_email", "Email not provided")
        
        hashtags = f"#hiring #{title.replace(' ', '')} #jobs"
        if job_details.get("skills"):
            hashtags += " " + " ".join([f"#{s.replace(' ', '')}" for s in job_details.get("skills")[:3]])

        post = f'''🚀 We are thrilled to announce that {company} is hiring for a new role! 📢

💼 **Position Details**
{position_details_str}

🎯 **Job Profile**
{job_profile_str}

🌟 **Why Join Us?**
{why_join_us_str}

📩 **Apply Now**
Link: {apply_link}
Email: {contact_email}

👇 Know someone who's a perfect fit? Tag them in the comments below!

{hashtags}
'''
        return post.strip()
    else:
        company = jobs[0].get("company_name", "our team")
        company_details = jobs[0].get("company_details", {})
        why_join_us = company_details.get("why_join_us", ["Great culture", "Competitive salary"])
        why_join_us_str = "\\n".join([f"✨ {bullet}" for bullet in why_join_us])
        apply_link = company_details.get("apply_link", "Link not provided")
        contact_email = company_details.get("contact_email", "Email not provided")
        
        locations = {}
        for job in jobs:
            loc = job.get('location') or 'Multiple Locations'
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(job)

        jobs_str = ""
        for loc, loc_jobs in locations.items():
            jobs_str += f"📍 {loc}\\n"
            for job in loc_jobs:
                jobs_str += f"• {job.get('title')}\\n"
            jobs_str += "\\n"

        post = f'''🚀 We are thrilled to announce that {company} is hiring across multiple locations! 📢

**Open Positions**

{jobs_str.strip()}

🌟 **Why Join Us?**
{why_join_us_str}

📩 **Apply Now**
Link: {apply_link}
Email: {contact_email}

👇 Know someone who's a perfect fit? Tag them in the comments below!

#hiring #jobs #career
'''
        return post.strip()
