# AI Resume Analyzer

## Overview

AI Resume Analyzer is a web application that helps job seekers evaluate their resumes against job descriptions. The application extracts resume content from PDF files, analyzes resume-job compatibility, calculates an ATS (Applicant Tracking System) score, and provides AI-powered feedback using Groq LLM.

---

## Features

### Resume Reader

* Upload a PDF resume.
* Extract and display resume content.
* Read resume text directly from the application.

### Job Matcher

* Compare a resume with a job description.
* Identify matching skills and qualifications.
* Generate AI-powered analysis.

### ATS Score Calculator

* Calculate resume compatibility with a job description.
* Display ATS score as a percentage.
* Help users optimize resumes for ATS systems.

### AI Resume Analysis

* Missing Skills Identification
* Strengths Analysis
* Weaknesses Analysis
* Improvement Suggestions
* ATS Compatibility Review

### Additional Tools

* Web Search Integration using Serper API
* Website Scraping using BeautifulSoup
* Groq LLM Integration for intelligent analysis

---

## Technologies Used

### Frontend

* Streamlit

### Backend

* FastAPI

### AI Model

* Groq
* Llama 3.3 70B Versatile

### Libraries

* PyPDF2
* Requests
* BeautifulSoup4
* Python Dotenv
* Pydantic

---

## Project Structure

```text
AI_Agent_Resume_Analyzer/

│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI_Agent_Resume_Analyzer.git
cd AI_Agent_Resume_Analyzer
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend folder.

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## Running the Backend

Navigate to backend folder:

```bash
cd backend
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
[https://ai-agent-resume-analyzer.onrender.com/](https://ai-agent-resume-analyzer.onrender.com/)
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Navigate to frontend folder:

```bash
cd frontend
```

Start Streamlit application:

```bash
streamlit run app.py
```

Frontend URL:

```text
[https://aiagentresumeanalyzer.streamlit.app/](https://aiagentresumeanalyzer.streamlit.app/)
```

---

## Application Workflow

1. User uploads a PDF resume.
2. Resume content is extracted using PyPDF2.
3. User enters a job description.
4. Resume and job description are sent to FastAPI backend.
5. Backend processes the request.
6. ATS score is calculated.
7. Groq LLM generates resume insights.
8. Results are displayed in Streamlit.

---

## API Endpoints

### Home

```http
GET /
```

### Resume Reader

```http
POST /agent/resume_reader
```

### Job Matcher

```http
POST /agent/job_matcher
```

### ATS Score

```http
POST /agent/ats_score
```

---

## Future Improvements

* Resume Ranking System
* Interview Question Generator
* Resume Download Feature
* Multiple Resume Comparison
* Semantic ATS Scoring
* Vector Database Integration
* RAG-based Resume Search
* Job Recommendation Engine

---

## Author

**Thirumal Jeegari**

GitHub:
https://github.com/ThirumalJeegari

LinkedIn:
https://linkedin.com/in/thirumaljeegari

---

## Author
Jeegari Thirumal
