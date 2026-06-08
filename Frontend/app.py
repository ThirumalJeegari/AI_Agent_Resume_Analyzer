import streamlit as st
import requests
from PyPDF2 import PdfReader

SERVER_URL = "https://ai-agent-resume-analyzer.onrender.com"


st.title("AI Resume Analyzer")

resume = st.file_uploader("Upload Resume",type="pdf")

job_description = st.text_area("Paste Job Description")


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

tab1, tab2, tab3 = st.tabs(["Resume Reader","Job Matcher","ATS Score"])


with tab1:

    if st.button("Read Resume"):
        res = requests.post(f"{SERVER_URL}/agent/resume_reader",json={"resume_text": resume_text,"job_description": job_description})
        data = res.json()
        st.subheader("Resume Content")
        st.write(data["result"])


with tab2:
    if st.button("Match Job"):
        res = requests.post(f"{SERVER_URL}/agent/job_matcher",json={"resume_text": resume_text,"job_description": job_description})
        data = res.json()
        st.subheader("Resume Analysis")
        st.write(data["result"])



with tab3:
    if st.button("Calculate ATS"):
        res = requests.post(f"{SERVER_URL}/agent/ats_score",json={"resume_text": resume_text,"job_description": job_description})
        st.metric("ATS Score",res.json()["result"])