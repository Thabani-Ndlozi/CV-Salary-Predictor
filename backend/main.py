from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.skill_extractor import extract_skills, calculate_effective_skills_count

import os
import io
import re
import fitz
import docx
import joblib
import pandas as pd


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "salary_model.pkl")

salary_model = joblib.load(MODEL_PATH)


class SalaryRequest(BaseModel):
    skills: list[str]
    experience_years: float
    education_level: str
    certifications: int
    job_title: str
    industry: str
    company_size: str
    location: str
    remote_work: str


@app.get("/")
def home():
    return {"message": "CV Salary Predictor API is running"}


def extract_text_from_pdf(file_bytes):
    text = ""
    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()
    return text


def extract_text_from_docx(file_bytes):
    text = ""
    document = docx.Document(io.BytesIO(file_bytes))

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_education_level(text):
    text = text.lower()

    if any(word in text for word in ["phd", "doctorate", "doctoral"]):
        return "PhD"

    if any(word in text for word in ["master", "masters", "msc", "mcom"]):
        return "Master"

    if any(word in text for word in ["bachelor", "degree", "bsc", "bcom", "btech", "bcomp"]):
        return "Bachelor"

    if any(word in text for word in ["diploma", "higher certificate"]):
        return "Bachelor"

    if any(word in text for word in ["matric", "high school", "grade 12"]):
        return "High School"

    return "Unknown"


def extract_certifications_count(text):
    text = text.lower()

    certification_keywords = [
        "certification",
        "certificate",
        "certified",
        "aws certified",
        "microsoft certified",
        "google certified",
        "cisco",
        "oracle certified",
    ]

    count = 0

    for keyword in certification_keywords:
        if keyword in text:
            count += 1

    return min(count, 10)


def extract_experience_years(text):
    text = text.lower()

    year_ranges = re.findall(r"(20\d{2})\s*[-–]\s*(20\d{2}|present|current)", text)

    total_years = 0

    for start, end in year_ranges:
        start_year = int(start)

        if end in ["present", "current"]:
            end_year = 2026
        else:
            end_year = int(end)

        years = end_year - start_year

        if 0 <= years <= 20:
            total_years += years

    explicit_match = re.search(r"(\d+)\+?\s*(years|yrs)\s+(of\s+)?experience", text)

    if explicit_match:
        return min(float(explicit_match.group(1)), 50)

    return min(float(total_years), 15)


def predict_salary(data: SalaryRequest):
    skills_count = calculate_effective_skills_count(data.skills)

    sample_data = pd.DataFrame([{
        "job_title": data.job_title,
        "experience_years": data.experience_years,
        "education_level": data.education_level,
        "skills_count": skills_count,
        "industry": data.industry,
        "company_size": data.company_size,
        "location": data.location,
        "remote_work": data.remote_work,
        "certifications": data.certifications,
    }])

    prediction = salary_model.predict(sample_data)[0]
    return round(float(prediction), 2)


def assess_cv_quality(extracted_text, detected_skills, experience_years, education_level, certifications):
    issues = []

    if len(extracted_text.strip()) < 500:
        issues.append("Your CV text is quite short, so the prediction may be less reliable.")

    if len(detected_skills) < 3:
        issues.append("Few technical skills were detected. Add more relevant tools, languages, and frameworks.")

    if experience_years == 0:
        issues.append("No clear years of experience were detected. Add dates to your work, projects, or internships.")

    if education_level == "Unknown":
        issues.append("No clear education level was detected.")

    if certifications == 0:
        issues.append("No certifications were detected. Certifications are not required, but they can strengthen your profile.")

    reliability_score = 100 - (len(issues) * 20)
    reliability_score = max(reliability_score, 20)

    return {
        "reliability_score": reliability_score,
        "issues": issues,
        "is_poor_cv": reliability_score < 60
    }

def is_likely_it_cv(extracted_text, detected_skills):
    text = extracted_text.lower()

    cv_keywords = [
        "curriculum vitae",
        "resume",
        "experience",
        "education",
        "skills",
        "projects",
        "employment",
        "work experience",
    ]

    it_keywords = [
        "software",
        "developer",
        "programming",
        "database",
        "frontend",
        "backend",
        "full stack",
        "web development",
        "api",
        "cloud",
        "data analyst",
        "machine learning",
        "cybersecurity",
        "network",
        "it support",
    ]

    cv_score = sum(1 for word in cv_keywords if word in text)
    it_score = sum(1 for word in it_keywords if word in text)
    skill_score = len(detected_skills)

    is_cv = cv_score >= 2
    is_it_related = it_score >= 2 or skill_score >= 4

    return {
        "is_valid": is_cv and is_it_related,
        "cv_score": cv_score,
        "it_score": it_score,
        "skill_score": skill_score,
    }


def generate_portfolio_suggestions(detected_skills):
    skills = set(skill.lower() for skill in detected_skills)
    suggestions = []

    if "git" not in skills and "github" not in skills:
        suggestions.append("Add Git and GitHub experience, including links to your repositories.")

    if "react" not in skills:
        suggestions.append("Build and showcase at least one React project with a clean user interface.")

    if "python" not in skills:
        suggestions.append("Add a Python project, especially one involving automation, APIs, data analysis, or machine learning.")

    if "sql" not in skills and "postgresql" not in skills and "mysql" not in skills:
        suggestions.append("Add database experience such as SQL, PostgreSQL, MySQL, or MongoDB.")

    if "fastapi" not in skills and "django" not in skills and "flask" not in skills:
        suggestions.append("Build a backend API project using FastAPI, Django, Flask, or Node.js.")

    if "docker" not in skills:
        suggestions.append("Learn basic Docker and containerise one of your full-stack projects.")

    if "aws" not in skills and "azure" not in skills and "google cloud" not in skills:
        suggestions.append("Deploy a project to the cloud and mention the hosting platform on your CV.")

    if len(suggestions) == 0:
        suggestions.append("Your technical profile looks strong. Improve further by adding measurable project impact and live demo links.")

    return suggestions[:5]


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_bytes)

    elif filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(file_bytes)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF or DOCX file.",
        )

    detected_skills = extract_skills(extracted_text)
    document_validation = is_likely_it_cv(extracted_text, detected_skills)

    experience_years = extract_experience_years(extracted_text)
    education_level = extract_education_level(extracted_text)
    certifications = extract_certifications_count(extracted_text)

    cv_quality = assess_cv_quality(
        extracted_text,
        detected_skills,
        experience_years,
        education_level,
        certifications
    )

    portfolio_suggestions = generate_portfolio_suggestions(detected_skills)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "CV analysed successfully. Confirm details to predict salary.",
        "skills": detected_skills,
        "experience_years": experience_years,
        "education_level": education_level,
        "certifications": certifications,
        "cv_quality": cv_quality,
        "portfolio_suggestions": portfolio_suggestions,
        "extracted_text": extracted_text[:3000],
        "document_validation": document_validation,
    }


@app.post("/predict-salary")
async def predict_salary_route(data: SalaryRequest):
    predicted_salary = predict_salary(data)

    return {
        "predicted_salary": predicted_salary,
        "currency": "USD",
        "salary_period": "Annual",
    }