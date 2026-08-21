import os
import json
import requests
from typing import Dict, Any

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://router.huggingface.co/v1/chat/completions"

def extract_job_details(text: str) -> Dict[str, Any]:
    """
    Extracts structured job details from raw JD text using AI.
    """
    if not HF_API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY is not set.")

    prompt = f"""
    You are an expert HR assistant. Extract the following job details from the provided unstructured job description text.
    Return ONLY a valid JSON object with the exact keys below. Do not add any markdown formatting or extra text.
    
    Keys:
    - title (string)
    - experience (string, e.g., "3+ years")
    - min_experience (integer or null, e.g., 3)
    - max_experience (integer or null)
    - location (string)
    - remote_type (string, exactly one of: "Remote", "Hybrid", "On-site")
    - skills (list of strings, return empty list if none)
    - salary (string or null, e.g., "$100k")
    - salary_max (string or null, e.g., "$120k")
    - salary_disclosure (string or null, e.g., "Show range")
    - description (string, a brief 2-3 sentence summary)
    - deadline (string or null, extract or guess a reasonable future date)
    - apply_link (string or null)
    - education_requirements (list of strings, return empty list if none)
    - match_threshold (float, default 30.0)
    - number_of_openings (integer or null)
    - role_objective (string or null, extract if explicitly mentioned)
    - key_responsibilities (list of strings, return empty list if none)
    - krm_measurement (string or null, extract Key Result Measurement if mentioned)
    - preferred_certifications (list of strings, return empty list if none)
    
    Job Description Text:
    {text}
    """

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.2,
        "stream": False,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            generated_text = result["choices"][0].get("message", {}).get("content", "").strip()
            # Clean up markdown codeblocks if present
            if "```json" in generated_text:
                generated_text = generated_text.split("```json")[1].split("```")[0].strip()
            elif "```" in generated_text:
                generated_text = generated_text.split("```")[1].split("```")[0].strip()
            
            try:
                data = json.loads(generated_text)
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON from AI response: {e}. Output: {generated_text[:200]}")
        else:
            raise ValueError("No choices returned from AI.")
    except Exception as e:
        print(f"Error extracting job details: {e}")
        raise

