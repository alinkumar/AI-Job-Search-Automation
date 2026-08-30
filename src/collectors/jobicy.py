import requests


def collect_jobicy(
    keywords="data analyst",
    max_jobs=20
):
    url = "https://jobicy.com/api/v2/remote-jobs"

    params = {
        "count": max_jobs,
        "tag": keywords
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
        job["_source"] = "Jobicy"

    return jobs[:max_jobs]