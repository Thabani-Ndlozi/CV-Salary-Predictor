import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    # Programming
    "python", "java", "javascript", "typescript", "c#", "c++", "php", "ruby",
    "kotlin", "swift", "go", "r",

    # Frontend
    "html", "css", "react", "vue", "angular", "bootstrap", "tailwind css",
    "next.js",

    # Backend
    "node.js", "express.js", "fastapi", "django", "flask", "spring boot",
    "asp.net",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "firebase", "sqlite",
    "oracle", "redis",

    # Data / ML
    "machine learning", "deep learning", "data analysis", "pandas", "numpy",
    "scikit-learn", "tensorflow", "keras", "pytorch", "matplotlib",
    "power bi", "excel",

    # Cloud / DevOps
    "git", "github", "docker", "kubernetes", "aws", "azure",
    "google cloud", "firebase hosting", "ci/cd",

    # General software
    "rest api", "api integration", "oop", "agile", "scrum",
    "software testing", "unit testing", "ui/ux",
]

SKILL_ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "react.js": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "ml": "machine learning",
    "gcp": "google cloud",
}


def extract_skills(text):
    text = text.lower()
    detected_skills = set()

    for alias, skill in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text):
            detected_skills.add(skill)

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            detected_skills.add(skill)

    return sorted(detected_skills)


def calculate_effective_skills_count(detected_skills):
    actual_count = len(detected_skills)

    # Diminishing returns: many skills should not keep increasing salary too much
    if actual_count <= 5:
        return actual_count
    elif actual_count <= 10:
        return 5 + ((actual_count - 5) * 0.5)
    else:
        return 7.5 + min((actual_count - 10) * 0.2, 2.5)