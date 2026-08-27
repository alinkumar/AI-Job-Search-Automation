def assess_job_quality(job):
    score = 0
    flags = []

    company = job.get("company", "").strip()
    description = job.get("description", "").strip()
    job_url = job.get("job_url", "").strip()
    eligibility = job.get("eligibility", "").strip()
    salary = job.get("salary", "").strip()

    if company:
        score += 20
    else:
        flags.append("company_missing")

    if job_url:
        score += 20
    else:
        flags.append("job_url_missing")

    if len(description) >= 100:
        score += 25
    elif description:
        score += 10
        flags.append("short_description")
    else:
        flags.append("description_missing")

    if eligibility:
        score += 20
    else:
        flags.append("eligibility_missing")

    if salary:
        score += 15

    if score >= 80:
        quality = "HIGH"
    elif score >= 60:
        quality = "MEDIUM"
    else:
        quality = "LOW"

    return {
        "quality_score": score,
        "quality": quality,
        "quality_flags": flags
    }