import re

SKILL_ALIASES = {
    "excel": "Microsoft Excel",
    "ms excel": "Microsoft Excel",
    "microsoft excel": "Microsoft Excel",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "python": "Python",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "xgboost": "XGBoost",
    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "deep-learning": "Deep Learning",
    "dl": "Deep Learning",
    "statistics": "Statistical Analysis",
    "statistical analysis": "Statistical Analysis",
    "eda": "Exploratory Data Analysis",
    "exploratory data analysis": "Exploratory Data Analysis",
    "data visualization": "Data Visualization",
    "data viz": "Data Visualization",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "git": "Git",
    "github": "GitHub",
}

ROLE_ALIASES = {
    "data analyst": "Data Analyst",
    "data analyst intern": "Data Analyst Intern",
    "data analytics intern": "Data Analytics Intern",
    "data analytics": "Data Analytics",
    "junior data analyst": "Junior Data Analyst",
    "jr data analyst": "Junior Data Analyst",
    "jr. data analyst": "Junior Data Analyst",
    "data science intern": "Data Science Intern",
    "data scientist intern": "Data Science Intern",
    "bi analyst": "BI Analyst",
    "business intelligence analyst": "BI Analyst",
    "reporting analyst": "Reporting Analyst",
    "mis analyst": "MIS Analyst",
    "analytics associate": "Analytics Associate",
}

LOCATION_ALIASES = {
    "new delhi": "Delhi",
    "delhi ncr": "Delhi NCR",
    "gurugram": "Gurgaon",
    "gurgaon": "Gurgaon",
    "noida": "Noida",
    "greater noida": "Greater Noida",
    "remote": "Remote",
    "work from home": "Remote",
    "wfh": "Remote",
}

def clean_text(value):
    if value is None:
        return ""

    value = str(value).strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def normalize_skill(skill):
    skill = clean_text(skill)
    return SKILL_ALIASES.get(skill, skill.title())


def normalize_skills(skills):
    if not skills:
        return []

    if isinstance(skills, str):
        skills = re.split(r",|;|\||\n", skills)

    normalized = []

    for skill in skills:
        skill = normalize_skill(skill)

        if skill and skill not in normalized:
            normalized.append(skill)

    return normalized


def normalize_role(role):
    role = clean_text(role)

    if role in ROLE_ALIASES:
        return ROLE_ALIASES[role]

    for alias, canonical in ROLE_ALIASES.items():
        if alias in role:
            return canonical

    return str(role).title()


def normalize_location(location):
    location = clean_text(location)

    if location in LOCATION_ALIASES:
        return LOCATION_ALIASES[location]

    if "remote" in location or "work from home" in location:
        return "Remote"

    if "gurugram" in location or "gurgaon" in location:
        return "Gurgaon"

    if "noida" in location:
        return "Noida"

    if "delhi" in location:
        return "Delhi"

    return str(location).title()


def normalize_experience(experience):
    experience = clean_text(experience)

    if not experience:
        return "Unknown"

    if any(term in experience for term in [
        "fresher",
        "freshers",
        "entry level",
        "entry-level",
        "intern",
        "internship",
        "0 years",
        "0-1",
        "0 - 1",
        "0-2",
        "0 - 2"
    ]):
        return "Fresher / Entry Level"

    match = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)\s*years?", experience)

    if match:
        return f"{match.group(1)}-{match.group(2)} years"

    match = re.search(r"(\d+)\+?\s*years?", experience)

    if match:
        return f"{match.group(1)}+ years"

    return experience


def normalize_work_mode(work_mode):
    work_mode = clean_text(work_mode)

    if any(term in work_mode for term in [
        "remote",
        "work from home",
        "wfh"
    ]):
        return "Remote"

    if "hybrid" in work_mode:
        return "Hybrid"

    if any(term in work_mode for term in [
        "on-site",
        "onsite",
        "office",
        "in office"
    ]):
        return "On-site"

    return "Unknown"


def normalize_job(job):
    normalized = job.copy()

    normalized["role"] = normalize_role(job.get("role"))
    normalized["location"] = normalize_location(job.get("location"))
    normalized["work_mode"] = normalize_work_mode(job.get("work_mode"))
    normalized["experience"] = normalize_experience(job.get("experience"))
    normalized["skills"] = normalize_skills(job.get("skills"))

    normalized["company"] = str(job.get("company", "")).strip()
    normalized["salary"] = str(job.get("salary", "")).strip()
    normalized["job_url"] = str(job.get("job_url", "")).strip()

    return normalized