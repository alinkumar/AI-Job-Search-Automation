import yaml

from src.collectors.multi_source import collect_all
from src.processing.batch_processor import process_batch
from src.storage.json_store import save_results
from src.storage.google_sheets import append_jobs
from src.storage.job_history import (
    filter_new_jobs,
    remember_jobs
)


def load_profile():
    with open(
        "config/profile.yaml",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def main():
    profile = load_profile()

    raw_jobs = collect_all()

    output = process_batch(
        raw_jobs,
        profile
    )

    results = output["results"]

    jobs = [
        result["job"]
        for result in results
    ]

    new_jobs, already_seen = filter_new_jobs(
        jobs
    )

    new_job_urls = {
        job.get("job_url", "")
        for job in new_jobs
        if job.get("job_url", "")
    }

    results = [
        result
        for result in results
        if result["job"].get("job_url", "")
        in new_job_urls
    ]

    output["results"] = results

    sheet_count = append_jobs(
        results
    )

    remember_jobs(
        new_jobs
    )

    file_path = save_results(
        output
    )

    decision_counts = {
        "APPLY": 0,
        "STRONG MATCH": 0,
        "REVIEW": 0,
        "CONSIDER": 0,
        "SKIP": 0,
        "DO NOT APPLY": 0
    }

    for result in results:
        decision = result["decision"].get(
            "decision",
            ""
        )

        if decision in decision_counts:
            decision_counts[decision] += 1

    actionable = (
        decision_counts["APPLY"]
        + decision_counts["STRONG MATCH"]
        + decision_counts["REVIEW"]
        + decision_counts["CONSIDER"]
    )

    source_counts = {}

    for item in raw_jobs:
        source = item.get(
            "_source",
            "Unknown"
        )

        source_counts[source] = (
            source_counts.get(source, 0) + 1
        )

    print("\n")
    print("=" * 64)
    print("AI JOB SEARCH AUTOMATION")
    print("=" * 64)

    for source, count in source_counts.items():
        print(
            f"{source.upper():20}"
            f"{count}"
        )

    print(
        f"RAW JOBS:            "
        f"{len(raw_jobs)}"
    )

    print(
        f"FINAL RESULTS:       "
        f"{len(results)}"
    )

    print(
        f"LOCATION REJECTED:   "
        f"{len(output['rejected_locations'])}"
    )

    print(
        f"ROLE REJECTED:       "
        f"{len(output['rejected_roles'])}"
    )

    print(
        f"EXPERIENCE REJECTED: "
        f"{len(output['rejected_experience'])}"
    )

    print(
        f"OLD:                 "
        f"{len(output['old_jobs'])}"
    )

    print(
        f"ALREADY SEEN:        "
        f"{len(already_seen)}"
    )

    print(
        f"DUPLICATES:          "
        f"{len(output['duplicates'])}"
    )

    print(
        f"REPOSTS:             "
        f"{len(output['possible_reposts'])}"
    )

    print("\n")
    print("=" * 64)
    print("DECISION SUMMARY")
    print("=" * 64)

    print(
        f"APPLY:               "
        f"{decision_counts['APPLY']}"
    )

    print(
        f"STRONG MATCH:        "
        f"{decision_counts['STRONG MATCH']}"
    )

    print(
        f"REVIEW:              "
        f"{decision_counts['REVIEW']}"
    )

    print(
        f"CONSIDER:            "
        f"{decision_counts['CONSIDER']}"
    )

    print(
        f"SKIP:                "
        f"{decision_counts['SKIP']}"
    )

    print(
        f"DO NOT APPLY:        "
        f"{decision_counts['DO NOT APPLY']}"
    )

    print(
        f"ACTIONABLE JOBS:     "
        f"{actionable}"
    )

    print("\n")
    print("=" * 64)
    print("RANKED RESULTS")
    print("=" * 64)

    if not results:
        print(
            "\nNo new actionable jobs found."
        )

    for index, result in enumerate(
        results,
        start=1
    ):
        job = result["job"]
        decision = result["decision"]

        print(
            f"\n{index}. "
            f"{job.get('company', '')} | "
            f"{job.get('role', '')}"
        )

        print(
            f"Source: "
            f"{job.get('source', '')}"
        )

        print(
            f"Location: "
            f"{job.get('location', '')}"
        )

        print(
            f"Experience: "
            f"{job.get('experience', '')}"
        )

        print(
            f"Skills: "
            f"{', '.join(job.get('skills', []))}"
        )

        print(
            f"Score: "
            f"{decision.get('match_score', '')} | "
            f"Risk: "
            f"{decision.get('risk', '')} | "
            f"Quality: "
            f"{decision.get('quality', '')}"
        )

        print(
            f"Decision: "
            f"{decision.get('decision', '')}"
        )

        print(
            f"URL: "
            f"{job.get('job_url', '')}"
        )

    print("\n")
    print("=" * 64)
    print(
        f"SAVED: {file_path}"
    )
    print(
        f"SHEET: {sheet_count} jobs added"
    )
    print("=" * 64)


if __name__ == "__main__":
    main()