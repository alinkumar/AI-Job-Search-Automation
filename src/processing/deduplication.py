import re
import hashlib
from difflib import SequenceMatcher


def normalize_text(text):
    text = str(text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_job_key(job):
    source = normalize_text(job.get("source"))
    job_id = normalize_text(job.get("job_id"))

    if source and job_id:
        return f"{source}|{job_id}"

    return ""


def get_url_key(job):
    return normalize_text(job.get("job_url"))


def get_company_role_location_key(job):
    company = normalize_text(job.get("company"))
    role = normalize_text(job.get("role"))
    location = normalize_text(job.get("location"))

    return f"{company}|{role}|{location}"


def get_description_hash(job):
    description = normalize_text(job.get("description"))

    if not description:
        return ""

    return hashlib.sha256(
        description.encode("utf-8")
    ).hexdigest()


def description_similarity(job_a, job_b):
    text_a = normalize_text(job_a.get("description"))
    text_b = normalize_text(job_b.get("description"))

    if not text_a or not text_b:
        return 0

    return SequenceMatcher(None, text_a, text_b).ratio()


def classify_job(job, seen_jobs):
    job_key = get_job_key(job)
    url_key = get_url_key(job)
    company_role_location = get_company_role_location_key(job)
    description_hash = get_description_hash(job)

    for seen in seen_jobs:

        if job_key and job_key == seen["job_key"]:
            return "DUPLICATE", "SAME SOURCE + JOB ID"

        if url_key and url_key == seen["url_key"]:
            return "DUPLICATE", "SAME JOB URL"

        if (
            company_role_location
            and company_role_location == seen["company_role_location"]
        ):
            return "POSSIBLE REPOST", "SAME COMPANY + ROLE + LOCATION"

        if (
            description_hash
            and description_hash == seen["description_hash"]
        ):
            return "DUPLICATE", "IDENTICAL DESCRIPTION"

        similarity = description_similarity(
            job,
            seen["job"]
        )

        if (
            company_role_location
            and company_role_location == seen["company_role_location"]
            and similarity >= 0.85
        ):
            return "POSSIBLE REPOST", "HIGH DESCRIPTION SIMILARITY"

    return "UNIQUE", None


def deduplicate_jobs(jobs):
    unique_jobs = []
    duplicates = []
    reposts = []
    seen_jobs = []

    for job in jobs:
        status, reason = classify_job(
            job,
            seen_jobs
        )

        record = {
            "job": job,
            "status": status,
            "reason": reason
        }

        if status == "UNIQUE":
            unique_jobs.append(job)

        elif status == "DUPLICATE":
            duplicates.append(record)

        elif status == "POSSIBLE REPOST":
            reposts.append(record)

        seen_jobs.append({
            "job": job,
            "job_key": get_job_key(job),
            "url_key": get_url_key(job),
            "company_role_location": get_company_role_location_key(job),
            "description_hash": get_description_hash(job)
        })

    return {
        "unique_jobs": unique_jobs,
        "duplicates": duplicates,
        "possible_reposts": reposts
    }