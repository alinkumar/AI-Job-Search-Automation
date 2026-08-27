import yaml

from src.collectors.multi_source import collect_adzuna, collect_muse
from src.processing.batch_processor import process_batch
from src.storage.json_store import save_results


def load_profile():
    with open(
        "config/profile.yaml",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file)


def main():
    profile = load_profile()

    roles = (
        profile["target_roles"]["primary"]
        + profile["target_roles"]["secondary"]
    )

    adzuna_jobs = collect_adzuna(
        roles,
        profile["preferred_locations"],
        pages=1,
        max_jobs=10
    )

    muse_jobs = collect_muse(
        ["Data and Analytics", "Data Science"],
        [
            "New Delhi, India",
            "Noida, India",
            "Gurgaon, India"
        ],
        levels=(
            "Entry Level",
            "Internship"
        ),
        pages=1
    )

    raw_jobs = adzuna_jobs + muse_jobs

    output = process_batch(
        raw_jobs,
        profile
    )

    file_path = save_results(output)

    results = output["results"]

    decision_counts = {
        "APPLY": 0,
        "STRONG MATCH": 0,
        "REVIEW": 0,
        "SKIP": 0,
        "DO NOT APPLY": 0
    }

    for result in results:
        decision = result["decision"]["decision"]

        if decision in decision_counts:
            decision_counts[decision] += 1

    actionable = (
        decision_counts["APPLY"]
        + decision_counts["STRONG MATCH"]
        + decision_counts["REVIEW"]
    )

    print("\n")
    print("=" * 64)
    print("AI JOB SEARCH AUTOMATION")
    print("=" * 64)

    print(f"ADZUNA:              {len(adzuna_jobs)}")
    print(f"THE MUSE:            {len(muse_jobs)}")
    print(f"RAW JOBS:            {len(raw_jobs)}")
    print(f"FINAL RESULTS:       {len(results)}")

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

    print(f"OLD:                 {len(output['old_jobs'])}")

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
        print("\nNo jobs passed all hard filters.")

    for index, result in enumerate(
        results,
        start=1
    ):
        job = result["job"]
        decision = result["decision"]

        print(
            f"\n{index}. "
            f"{job['company']} | "
            f"{job['role']}"
        )

        print(
            f"Location: "
            f"{job['location']}"
        )

        print(
            f"Experience: "
            f"{job['experience']}"
        )

        print(
            f"Skills: "
            f"{', '.join(job['skills'])}"
        )

        print(
            f"Score: "
            f"{decision['match_score']} | "
            f"Risk: "
            f"{decision['risk']} | "
            f"Quality: "
            f"{decision['quality']}"
        )

        print(
            f"Decision: "
            f"{decision['decision']}"
        )

        print(
            f"URL: "
            f"{job['job_url']}"
        )

    print("\n")
    print("=" * 64)
    print(f"SAVED: {file_path}")
    print("=" * 64)


if __name__ == "__main__":
    main()