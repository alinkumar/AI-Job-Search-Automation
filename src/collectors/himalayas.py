import requests


def collect_himalayas(
    keywords="data analyst",
    page=1,
    max_jobs=20
):
    url = "https://himalayas.app/jobs/api"

    params = {
        "q": keywords,
        "page": page
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
        job["_source"] = "Himalayas"

    return jobs[:max_jobs]