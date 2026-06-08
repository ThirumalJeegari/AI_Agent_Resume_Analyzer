import streamlit as st
import requests
from PyPDF2 import PdfReader

SERVER_URL = "https://your-render-url.onrender.com"

st.title("AI Resume Analyzer Agent")

resume = st.file_uploader(
    "Upload Resume",
    type="pdf"
)

job_description = st.text_area(
    "Paste Job Description"
)

query = st.text_input(
    "Ask the Agent"
)

def read_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


resume_text = ""

if resume:
    resume_text = read_pdf(resume)


if st.button("Run Agent"):

    response = requests.post(
        f"{SERVER_URL}/agent",
        json={
            "user_query": query,
            "resume_text": resume_text,
            "job_description": job_description
        }
    )

    st.json(response.json())