import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-4o-mini"


def analyze_resume(resume_text, job_description):
    """
    Analyze Resume against Job Description using OpenRouter.
    Returns a Python dictionary.
    """

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and HR Recruiter.

Compare the Resume with the Job Description.

Return ONLY valid JSON.

Resume:
{resume_text}

Job Description:
{job_description}

JSON format:

{{
    "score":85,
    "verdict":"Strong",
    "matching_skills":[
        "Python",
        "Machine Learning",
        "SQL"
    ],
    "missing_skills":[
        "Docker",
        "AWS"
    ],
    "strengths":[
        "Strong Python knowledge",
        "Relevant Projects",
        "Good Communication"
    ],
    "suggestions":[
        "Add AWS experience",
        "Mention quantified achievements",
        "Improve ATS keywords"
    ],
    "recommendation":"Highly Recommended"
}}

Return ONLY JSON.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an ATS Resume Screening AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content.strip()

        # Remove markdown if AI returns ```json
        answer = answer.replace("```json", "")
        answer = answer.replace("```", "")
        answer = answer.strip()

        return json.loads(answer)

    except Exception as e:

        return {
            "score": 0,
            "verdict": "Error",
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "suggestions": [str(e)],
            "recommendation": "Analysis Failed"
        }