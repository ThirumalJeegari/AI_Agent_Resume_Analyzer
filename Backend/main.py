from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import requests
import os
from bs4 import BeautifulSoup

load_dotenv()

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer Agent Running"}


class AgentRequest(BaseModel):
    user_query: str
    resume_text: str = ""
    job_description: str = ""



def ats_tool(resume, job):

    resume_words = set(resume.lower().split())
    job_words = set(job.lower().split())

    if len(job_words) == 0:
        return 0

    matched = resume_words.intersection(job_words)

    score = (len(matched) / len(job_words)) * 100

    return round(score, 2)


def rag_tool(resume):
    return resume[:3000]


def web_search_tool(query):

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"q": query}

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()


def scrape_tool(url):

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:3000]

    except Exception as e:
        return str(e)


def llm_tool(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def analyze_resume_tool(resume, job, ats_score):

    prompt = f""" Resume : {resume} Job Description : {job} ATS Score : {ats_score}

        Analyze the resume.

        Provide:

        1. ATS Compatibility Score
        2. Missing Skills
        3. Strengths
        4. Weaknesses
        5. Suggestions
        6. Final Verdict
    """

    return llm_tool(prompt)



def resume_agent(user_query, resume, job):

    planner_prompt = f"""
        You are an AI Resume Agent.

        Available Tools:

        1. ATS_TOOL
        - Calculates ATS score

        2. RESUME_READER
        - Reads resume

        3. JOB_MATCHER
        - Analyzes resume against job description

        User Query : {user_query}

        Return ONLY one of:

        ATS_TOOL
        RESUME_READER
        JOB_MATCHER
        FULL_ANALYSIS
    """

    decision = llm_tool(planner_prompt).strip().upper()

    print("Agent Decision:", decision)

    if "ATS_TOOL" in decision:

        return {
            "tool_used": "ATS_TOOL",
            "result": ats_tool(resume, job)
        }

    elif "RESUME_READER" in decision:

        return {
            "tool_used": "RESUME_READER",
            "result": rag_tool(resume)
        }

    elif "JOB_MATCHER" in decision:

        ats = ats_tool(resume, job)

        result = analyze_resume_tool(resume,job,ats)

        return {
            "tool_used": "JOB_MATCHER",
            "result": result
        }

    else:

        ats = ats_tool(resume, job)

        analysis = analyze_resume_tool(resume,job,ats)

        return {
            "tool_used": "FULL_ANALYSIS",
            "ats_score": ats,
            "analysis": analysis
        }



@app.post("/agent")
def run_agent(data: AgentRequest):

    result = resume_agent(
        data.user_query,
        data.resume_text,
        data.job_description
    )

    return result