import json
import os


HISTORY_FILE = "data/job_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return set()

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return {
                str(url).strip()
                for url in data
                if str(url).strip()
            }

        return set()

    except (
        json.JSONDecodeError,
        OSError
    ):
        return set()


def save_history(urls):
    os.makedirs(
        os.path.dirname(HISTORY_FILE),
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            sorted(urls),
            file,
            indent=2,
            ensure_ascii=False
        )


def filter_new_jobs(jobs):
    history = load_history()

    new_jobs = []
    already_seen = []

    for job in jobs:
        url = str(
            job.get(
                "job_url",
                ""
            )
        ).strip()

        if not url:
            new_jobs.append(job)
            continue

        if url in history:
            already_seen.append(job)
        else:
            new_jobs.append(job)

    return (
        new_jobs,
        already_seen
    )


def remember_jobs(jobs):
    history = load_history()

    for job in jobs:
        url = str(
            job.get(
                "job_url",
                ""
            )
        ).strip()

        if url:
            history.add(url)

    save_history(
        history
    )