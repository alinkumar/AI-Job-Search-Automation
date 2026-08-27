import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api"


def search_jobs(query, location, page=1, results_per_page=20):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Adzuna API credentials not found")

    url = f"{BASE_URL}/jobs/in/search/{page}"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()