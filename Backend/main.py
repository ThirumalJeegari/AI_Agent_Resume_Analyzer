from fastapi import FastAPI
import requests
from dotenv import load_dotenv
from groq import Groq
import os
from pydantic import BaseModel
from bs4 import BeautifulSoup

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer Backend Running"
    }


class AgentRequest(BaseModel):
    resume_text: str = ""
    job_description: str = ""


def ats_tool(resume,job):
    resume_words = resume.lower().split()
    job_words = job.lower().split()
    matched = []
    for word in job_words:
        if word in resume_words and word not in matched:
            matched.append(word)

    if len(job_words) == 0:
        return 0

    score = (len(matched)/len(set(job_words))) * 100
    return round(score, 2)


def rag_tool(resume):
    return resume


def web_search_tool(query):

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY,"Content-Type": "application/json"}
    payload = {"q": query}
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    return response.json()


def scrape_tool(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        text = soup.get_text(separator=" ",strip=True)
        return text[:3000]

    except Exception as e:
        return str(e)


def llm_tool(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content


def analyze_resume_tool(resume,job):

    prompt = f""" Resume : {resume} Job Description : {job}

            Analyze the resume.

            Give:

            1. ATS Compatibility Score
            2. Missing Skills
            3. Strengths
            4. Weaknesses
            5. Suggestions
        """

    return llm_tool(prompt)


@app.post("/agent/resume_reader")
def resume_reader(data: AgentRequest):

    return {
        "result":rag_tool(
            data.resume_text
        )
    }


@app.post("/agent/job_matcher")
def job_matcher(data: AgentRequest):

    return {
        "result":analyze_resume_tool(
            data.resume_text,
            data.job_description
        )
    }


@app.post("/agent/ats_score")
def ats_score(
    data: AgentRequest
):

    return {
        "result":
        ats_tool(
            data.resume_text,
            data.job_description
        )
    }