# backend/backend_api.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json

# #import modelss
from backend.helper import configure_genai, extract_pdf_text, prepare_prompt, get_gemini_response

# Try to load from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# If API key is not found in .env, use the hardcoded one
if not api_key:
    api_key = "AIzaSyDwqxrKMIOstqjTmkiiB67taeTRMYRg96E"

print(f"Using API key: {api_key}")
configure_genai(api_key)

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, use specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test/")
async def test_endpoint():
    return {"status": "ok", "message": "API is working"}

@app.post("/analyze-resume/")
async def analyze_resume(resume: UploadFile, jd: str = Form(...)):
    try:
        print(f"Received request with JD: {jd[:50]}...")
        print(f"Resume filename: {resume.filename}")

        resume_text = extract_pdf_text(resume.file)
        print(f"Extracted resume text: {resume_text[:100]}...")

        prompt = prepare_prompt(resume_text, jd)
        print(f"Prepared prompt: {prompt[:100]}...")

        response = get_gemini_response(prompt)
        print(f"Got response: {response[:100]}...")

        result = json.loads(response)
        print(f"Parsed result: {result}")

        return result
    except Exception as e:
        print(f"Error in analyze_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
