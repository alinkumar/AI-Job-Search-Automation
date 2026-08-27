from datetime import datetime
from src.processing.work_mode import detect_work_mode
from src.processing.job_parser import parse_job_description


def extract_salary(job):
    salary_min = job.get("salary_min", 0) or 0
    salary_max = job.get("salary_max", 0) or 0

    if salary_min and salary_max:
        return f"₹{salary_min:,.0f} - ₹{salary_max:,.0f}"

    if salary_max:
        return f"Up to ₹{salary_max:,.0f}"

    if salary_min:
        return f"From ₹{salary_min:,.0f}"

    return "Not disclosed"


def extract_company(job):
    company = job.get("company", {})

    if isinstance(company, dict):
        return company.get("display_name", "")

    return str(company or "")


def extract_location(job):
    location = job.get("location", {})

    if isinstance(location, dict):
        return location.get("display_name", "")

    return str(location or "")


def extract_posted_date(job):
    created = job.get("created")

    if not created:
        return ""

    try:
        return datetime.fromisoformat(
            created.replace("Z", "+00:00")
        ).isoformat()
    except ValueError:
        return ""


def transform_adzuna_job(job):
    description = job.get("description", "") or ""
    role = job.get("title", "")
    location = extract_location(job)

    parsed = parse_job_description(description)

    return {
        "job_id": f"adzuna_{job.get('id')}",
        "source": "Adzuna",
        "company": extract_company(job),
        "role": role,
        "location": location,
        "work_mode": detect_work_mode({
            "role": role,
            "location": location,
            "description": description
        }),
        "salary": extract_salary(job),
        "skills": parsed["skills"],
        "description": description,
        "job_url": job.get("redirect_url", ""),
        "posted_date": extract_posted_date(job),
        "experience": parsed["experience"],
        "eligibility": parsed["eligibility"]
    }