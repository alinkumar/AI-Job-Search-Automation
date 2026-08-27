import re
from datetime import datetime

from src.processing.work_mode import detect_work_mode
from src.processing.job_parser import parse_job_description


def clean_description(contents):
    text = str(contents or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_salary(job):
    salary = job.get("salary")

    if salary:
        return str(salary)

    return "Not disclosed"


def extract_location(job):
    locations = job.get("locations", [])

    if not locations:
        return ""

    names = []

    for location in locations:
        if isinstance(location, dict):
            name = location.get("name")

            if name:
                names.append(name)

    return ", ".join(names)


def extract_posted_date(job):
    date = job.get("publication_date")

    if not date:
        return ""

    try:
        return datetime.fromisoformat(
            date.replace("Z", "+00:00")
        ).isoformat()
    except ValueError:
        return ""


def extract_company(job):
    company = job.get("company", {})

    if isinstance(company, dict):
        return company.get("name", "")

    return str(company or "")


def transform_muse_job(job):
    description = clean_description(
        job.get("contents", "")
    )

    role = job.get("name", "")
    location = extract_location(job)

    parsed = parse_job_description(description)

    work_mode = detect_work_mode({
        "role": role,
        "location": location,
        "description": description
    })

    return {
        "job_id": f"muse_{job.get('id')}",
        "source": "The Muse",
        "company": extract_company(job),
        "role": role,
        "location": location,
        "work_mode": work_mode,
        "salary": extract_salary(job),
        "skills": parsed["skills"],
        "description": description,
        "job_url": job.get("refs", {}).get("landing_page", ""),
        "posted_date": extract_posted_date(job),
        "experience": parsed["experience"],
        "eligibility": parsed["eligibility"]
    }