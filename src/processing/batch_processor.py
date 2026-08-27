from src.processing.transform import transform_adzuna_job
from src.processing.transform_muse import transform_muse_job
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


def transform_job(raw_job, source):
    if source == "Adzuna":
        return transform_adzuna_job(raw_job)

    if source == "The Muse":
        return transform_muse_job(raw_job)

    raise ValueError(f"Unsupported source: {source}")


def prepare_jobs(raw_jobs):
    transformed_jobs = []

    for item in raw_jobs:
        source = item.get("_source")

        if not source:
            continue

        raw_job = item.get("job", item)

        try:
            job = transform_job(raw_job, source)
        except Exception:
            continue

        if not job.get("description"):
            parsed = {
                "skills": [],
                "experience": "Unknown",
                "eligibility": "Verify required"
            }
        else:
            parsed = parse_job_description(
                job["description"]
            )

        if not job.get("skills"):
            job["skills"] = parsed["skills"]

        if not job.get("experience"):
            job["experience"] = parsed["experience"]

        if not job.get("eligibility"):
            job["eligibility"] = parsed["eligibility"]

        transformed_jobs.append(job)

    return transformed_jobs


def process_batch(raw_jobs, profile):
    jobs = prepare_jobs(raw_jobs)

    eligible_jobs = []
    rejected_locations = []
    rejected_roles = []
    rejected_experience = []
    old_jobs = []

    target_roles = (
        profile["target_roles"]["primary"]
        + profile["target_roles"]["secondary"]
    )

    for job in jobs:
        location_result = check_location_eligibility(job)
        job["_location"] = location_result

        if not location_result["eligible"]:
            rejected_locations.append(job)
            continue

        if not filter_role(job, target_roles):
            rejected_roles.append(job)
            continue

        experience_result = check_experience_eligibility(
            job,
            profile
        )
        job["_experience"] = experience_result

        if experience_result["status"] != "COMPATIBLE":
            rejected_experience.append(job)
            continue

        freshness = check_freshness(
            job["posted_date"]
        )
        job["_freshness"] = freshness

        if freshness["fresh"]:
            eligible_jobs.append(job)
        else:
            old_jobs.append(job)

    dedup_result = deduplicate_jobs(
        eligible_jobs
    )

    candidates = dedup_result["unique_jobs"]

    results = []

    for job in candidates:
        risk = detect_scam_risk(job)

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

        quality = assess_job_quality(job)

        decision = make_final_decision(
            match_result,
            quality
        )

        results.append({
            "job": job,
            "location": job["_location"],
            "experience": job["_experience"],
            "freshness": job["_freshness"],
            "match": match_result,
            "quality": quality,
            "decision": decision
        })

    results = rank_results(results)

    return {
        "results": results,
        "rejected_locations": rejected_locations,
        "rejected_roles": rejected_roles,
        "rejected_experience": rejected_experience,
        "old_jobs": old_jobs,
        "duplicates": dedup_result["duplicates"],
        "possible_reposts": dedup_result["possible_reposts"]
    }