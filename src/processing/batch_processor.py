from src.processing.transform import transform_job
from src.processing.job_parser import parse_job_description
from src.processing.freshness import check_freshness
from src.processing.deduplication import deduplicate_jobs
from src.processing.location_eligibility import check_location_eligibility
from src.processing.experience_eligibility import check_experience_eligibility
from src.processing.scam_detector import detect_scam_risk
from src.processing.quality import assess_job_quality
from src.processing.filters import filter_role

from src.matching.score import calculate_match_score
from src.matching.match_result import build_match_result
from src.matching.decision import make_final_decision
from src.matching.ranking import rank_results


def prepare_jobs(raw_jobs):
    transformed_jobs = []

    for item in raw_jobs:
        source = item.get("_source")

        if not source:
            continue

        raw_job = item.get(
            "job",
            item
        )

        try:
            job = transform_job(
                raw_job,
                source
            )
        except Exception:
            continue

        description = job.get(
            "description",
            ""
        )

        if description:
            try:
                parsed = parse_job_description(
                    description,
                    job.get(
                        "role",
                        ""
                    )
                )
            except TypeError:
                parsed = parse_job_description(
                    description
                )
        else:
            parsed = {
                "skills": [],
                "experience": "Unknown",
                "eligibility": "Verify required"
            }

        if not job.get("skills"):
            job["skills"] = parsed.get(
                "skills",
                []
            )

        if not job.get("experience"):
            job["experience"] = parsed.get(
                "experience",
                "Unknown"
            )

        if not job.get("eligibility"):
            job["eligibility"] = parsed.get(
                "eligibility",
                "Verify required"
            )

        transformed_jobs.append(
            job
        )

    return transformed_jobs


def process_batch(raw_jobs, profile):
    jobs = prepare_jobs(
        raw_jobs
    )

    eligible_jobs = []

    rejected_locations = []
    rejected_roles = []
    rejected_experience = []
    old_jobs = []

    target_roles = (
        profile.get(
            "target_roles",
            {}
        ).get(
            "primary",
            []
        )
        +
        profile.get(
            "target_roles",
            {}
        ).get(
            "secondary",
            []
        )
    )

    for job in jobs:

        location_result = check_location_eligibility(
            job
        )

        job["_location"] = location_result

        if not location_result.get(
            "eligible",
            False
        ):
            rejected_locations.append(
                job
            )
            continue

        if not filter_role(
            job,
            target_roles
        ):
            rejected_roles.append(
                job
            )
            continue

        experience_result = check_experience_eligibility(
            job,
            profile
        )

        job["_experience"] = experience_result

        if experience_result.get(
            "status"
        ) == "INCOMPATIBLE":
            rejected_experience.append(
                job
            )
            continue

        freshness = check_freshness(
            job.get(
                "posted_date",
                ""
            )
        )

        job["_freshness"] = freshness

        if freshness.get(
            "fresh",
            False
        ):
            eligible_jobs.append(
                job
            )
        else:
            old_jobs.append(
                job
            )

    dedup_result = deduplicate_jobs(
        eligible_jobs
    )

    candidates = dedup_result.get(
        "unique_jobs",
        []
    )

    results = []

    for job in candidates:

        risk = detect_scam_risk(
            job
        )

        score = calculate_match_score(
            job,
            profile
        )

        match_result = build_match_result(
            job,
            profile,
            score,
            risk
        )

        quality_result = assess_job_quality(
            job
        )

        decision = make_final_decision(
            match_result,
            quality_result
        )

        results.append({
            "job": job,
            "location": job.get(
                "_location",
                {}
            ),
            "experience": job.get(
                "_experience",
                {}
            ),
            "freshness": job.get(
                "_freshness",
                {}
            ),
            "match": match_result,
            "quality": quality_result,
            "decision": decision
        })

    results = rank_results(
        results
    )

    return {
        "results": results,
        "rejected_locations": rejected_locations,
        "rejected_roles": rejected_roles,
        "rejected_experience": rejected_experience,
        "old_jobs": old_jobs,
        "duplicates": dedup_result.get(
            "duplicates",
            []
        ),
        "possible_reposts": dedup_result.get(
            "possible_reposts",
            []
        )
    }