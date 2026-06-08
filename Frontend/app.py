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

    try:

        response = requests.post(
            f"{SERVER_URL}/agent",
            json={
                "user_query": query,
                "resume_text": resume_text,
                "job_description": job_description
            },
            timeout=60
        )

        st.write("Status Code:", response.status_code)

        data = response.json()

        st.subheader("Agent Response")

        # Show complete response
        st.json(data)

        # Optional pretty display
        if "tool_used" in data:
            st.success(f"Tool Used: {data['tool_used']}")

        if "result" in data:
            st.write(data["result"])

        if "ats_score" in data:
            st.metric("ATS Score", data["ats_score"])

        if "analysis" in data:
            st.write(data["analysis"])

    except Exception as e:
        st.error(f"Error: {str(e)}")