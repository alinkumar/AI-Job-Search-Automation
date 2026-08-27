from src.collectors.adzuna import search_jobs as search_adzuna
from src.collectors.the_muse import search_jobs as search_muse


def collect_adzuna(roles, locations, pages=3, max_jobs=50):
    jobs = []
    seen = set()

    for role in roles:
        for location in locations:
            for page in range(1, pages + 1):
                try:
                    data = search_adzuna(
                        role,
                        location,
                        page=page,
                        results_per_page=max_jobs
                    )

                    for job in data.get("results", []):
                        job_id = str(job.get("id", ""))

                        if job_id and job_id in seen:
                            continue

                        if job_id:
                            seen.add(job_id)

                        jobs.append({
                            "_source": "Adzuna",
                            "job": job
                        })

                except Exception:
                    continue

    return jobs


def collect_muse(
    categories,
    locations,
    levels=("Entry Level", "Internship"),
    pages=2
):
    jobs = []
    seen = set()

    for category in categories:
        for location in locations:
            for level in levels:
                for page in range(pages):
                    try:
                        data = search_muse(
                            category=category,
                            location=location,
                            level=level,
                            page=page
                        )

                        for job in data.get("results", []):
                            job_id = str(job.get("id", ""))

                            if job_id and job_id in seen:
                                continue

                            if job_id:
                                seen.add(job_id)

                            jobs.append({
                                "_source": "The Muse",
                                "job": job
                            })

                    except Exception:
                        continue

    return jobs


def collect_all():
    roles = [
        "Data Analyst",
        "Data Analyst Intern",
        "Junior Data Analyst",
        "Data Analytics Intern",
        "Data Science Intern",
        "BI Analyst",
        "Reporting Analyst",
        "MIS Analyst",
        "Analytics Associate"
    ]

    locations = [
        "Delhi",
        "Noida",
        "Gurgaon",
        "Remote"
    ]

    adzuna_jobs = collect_adzuna(
        roles,
        locations,
        pages=3,
        max_jobs=50
    )

    muse_jobs = collect_muse(
        ["Data and Analytics", "Data Science"],
        [
            "New Delhi, India",
            "Noida, India",
            "Gurgaon, India",
            "Hyderabad, India"
        ],
        levels=("Entry Level", "Internship"),
        pages=2
    )

    return adzuna_jobs + muse_jobs