import requests


def collect_remotive(
    search="data analyst",
    max_jobs=20
):
    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": search
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    jobs = data.get("jobs", [])

    for job in jobs:
        job["_source"] = "Remotive"

    return jobs[:max_jobs]