# backend/backend_api.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json

from helper import configure_genai, extract_pdf_text, prepare_prompt, get_gemini_response

load_dotenv()
configure_genai(os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, use specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-resume/")
async def analyze_resume(resume: UploadFile, jd: str = Form(...)):
    try:
        resume_text = extract_pdf_text(resume.file)
        prompt = prepare_prompt(resume_text, jd)
        response = get_gemini_response(prompt)
        return json.loads(response)
    except Exception as e:
        return {"error": str(e)}
