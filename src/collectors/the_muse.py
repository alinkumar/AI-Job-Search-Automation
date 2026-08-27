import os
import requests
from dotenv import load_dotenv


load_dotenv()


BASE_URL = "https://www.themuse.com/api/public/jobs"


def search_jobs(
    category="Data and Analytics",
    location=None,
    level=None,
    page=0
):
    api_key = os.getenv("THE_MUSE_API_KEY")

    if not api_key:
        raise RuntimeError("THE_MUSE_API_KEY not found")

    params = {
        "api_key": api_key,
        "page": page,
        "category": category
    }

    if location:
        params["location"] = location

    if level:
        params["level"] = level

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()