import os
import requests
from dotenv import load_dotenv

load_dotenv()


def clean_value(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join(
            clean_value(item)
            for item in value
            if clean_value(item)
        )

    if isinstance(value, dict):
        for key in [
            "name",
            "title",
            "display_name",
            "text",
            "value"
        ]:
            if value.get(key):
                return clean_value(
                    value.get(key)
                )

        return ""

    return str(value).strip()


def normalize_jooble_job(job):
    return {
        "id": clean_value(
            job.get("id")
            or job.get("jobId")
            or job.get("guid")
        ),
        "title": clean_value(
            job.get("title")
            or job.get("position")
            or job.get("role")
        ),
        "company": clean_value(
            job.get("company")
            or job.get("companyName")
            or job.get("employer")
        ),
        "location": clean_value(
            job.get("location")
            or job.get("city")
            or job.get("place")
        ),
        "description": clean_value(
            job.get("snippet")
            or job.get("description")
            or job.get("content")
            or job.get("details")
            or job.get("jobDescription")
        ),
        "url": clean_value(
            job.get("link")
            or job.get("url")
            or job.get("jobUrl")
            or job.get("redirect_url")
        ),
        "salary": clean_value(
            job.get("salary")
            or job.get("salaryRange")
            or job.get("compensation")
        ),
        "created": clean_value(
            job.get("updated")
            or job.get("created")
            or job.get("createdAt")
            or job.get("published")
            or job.get("posted")
        ),
        "_source": "Jooble"
    }


def collect_jooble(
    roles,
    locations,
    pages=1,
    max_jobs=30
):
    api_key = os.getenv(
        "JOOBLE_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "JOOBLE_API_KEY not found in .env"
        )

    url = (
        f"https://in.jooble.org/api/"
        f"{api_key}"
    )

    jobs = []
    seen = set()

    for role in roles:
        for location in locations:

            payload = {
                "keywords": role,
                "location": location,
                "page": 1
            }

            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

            except Exception:
                continue

            for raw_job in data.get(
                "jobs",
                []
            ):
                job = normalize_jooble_job(
                    raw_job
                )

                job_id = (
                    job.get("id")
                    or job.get("url")
                )

                if not job_id:
                    continue

                if job_id in seen:
                    continue

                seen.add(job_id)

                jobs.append(job)

                if len(jobs) >= max_jobs:
                    return jobs

    return jobs