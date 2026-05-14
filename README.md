# CV Salary Predictor

AI-powered web application that analyzes IT/software-related CVs, extracts technical skills and experience, and predicts estimated salary benchmarks using Machine Learning.

---

## Repository Description

AI-powered CV analysis and salary prediction web app for IT/software-related careers using React, FastAPI, NLP, and Machine Learning.

---

# Overview

CV Salary Predictor is a full-stack Machine Learning project designed to analyze CVs/resumes for software and IT-related careers.

The system extracts information from uploaded PDF or DOCX CVs, identifies technical skills using NLP, estimates years of experience and education level, validates whether the uploaded document is an IT-related CV, and generates AI-based salary predictions.

The application also provides:

* CV quality analysis
* Portfolio improvement suggestions
* Skill extraction
* Salary prediction in USD and ZAR
* Monthly and yearly salary estimates
* IT CV validation checks

This project combines:

* Frontend Development
* Backend API Development
* Natural Language Processing (NLP)
* Machine Learning
* Full-stack Integration
* UI/UX Design

---

# Screenshots

## Home Page

<img width="1888" height="966" alt="image" src="https://github.com/user-attachments/assets/0a7ac3d4-9584-44b6-ae6f-dc34737e4533" />


## CV Analysis

<img width="573" height="866" alt="Screenshot 2026-05-14 022529" src="https://github.com/user-attachments/assets/273076fe-381c-4849-80a5-4a6eb9838b50" />


## Salary Prediction

<img width="598" height="815" alt="image" src="https://github.com/user-attachments/assets/fabaad90-af68-4b69-8f21-759cd6bcacbd" />


## Invalid Document Detection

<img width="602" height="852" alt="image" src="https://github.com/user-attachments/assets/a7ebcbd1-27f4-4d0f-af52-d4a98c238b57" />


---

# Features

* Upload CVs in PDF or DOCX format
* Extract CV text automatically
* Detect technical skills using NLP
* Estimate years of experience
* Detect education level
* Detect certifications
* Validate whether uploaded file is an IT-related CV
* AI-generated salary prediction
* USD and ZAR salary conversion
* Monthly and yearly salary estimates
* CV quality scoring
* Portfolio improvement recommendations
* Responsive modern UI
* Loading states and validation

---

# Tech Stack

## Frontend

* React
* Axios
* CSS
* Vite

## Backend

* FastAPI
* Python
* spaCy
* scikit-learn
* Pandas
* PyMuPDF
* python-docx

## Machine Learning

* Random Forest Regressor
* NLP-based skill extraction
* Feature engineering
* Salary prediction model

---

# How It Works

## Step 1 — Upload CV

The user uploads a PDF or DOCX CV.

## Step 2 — CV Processing

The backend extracts text from the uploaded file.

## Step 3 — NLP Analysis

The application analyzes the text and detects:

* Technical skills
* Education level
* Years of experience
* Certifications

## Step 4 — CV Validation

The system checks whether the uploaded document appears to be an IT/software-related CV.

## Step 5 — Salary Prediction

The Machine Learning model predicts estimated salary benchmarks based on:

* Skills
* Experience
* Education
* Career context selected by the user

## Step 6 — Recommendations

The application provides:

* CV quality feedback
* Portfolio-building suggestions
* Skill improvement recommendations

---

# Folder Structure

```text
CV-Salary-Predictor/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── data/
│   │   └── salaries.csv
│   ├── model/
│   │   └── train_model.py
│   ├── notebooks/
│   │   └── data_cleaning.ipynb
│   └── services/
│       └── skill_extractor.py
│
├── frontend/
│   ├── package.json
│   ├── src/
│   └── public/
│
├── README.md
└── .gitignore
```

---

# Backend Setup

```powershell
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python -m spacy download en_core_web_sm

python model/train_model.py

uvicorn main:app --reload
```

---

# Frontend Setup

```powershell
cd frontend

npm install

npm run dev
```

---

# Model Training

The trained Machine Learning model file (`salary_model.pkl`) is not included in this repository because of its large size.

To generate the model:

1. Run the notebook in `backend/notebooks/`
   OR
2. Run:

```powershell
python model/train_model.py
```

This will generate:

```text
backend/model/salary_model.pkl
```

---

# Important Notes

* This application is designed primarily for IT/software-related careers.
* Salary predictions are AI-generated estimates and should not be considered guaranteed compensation figures.
* Non-IT CVs may be rejected by the validation system.
* Salary conversion values are approximate.

---

# Future Improvements

* Real-time exchange rates
* Improved NLP extraction
* Country-specific salary models
* Better experience parsing
* AI-generated career roadmap suggestions
* Cloud deployment

---

# Author

Created by **Thabani Ndlozi**

* GitHub: [https://github.com/Thabani-Ndlozi](https://github.com/Thabani-Ndlozi)

---

# License

This project is for educational and portfolio purposes.
