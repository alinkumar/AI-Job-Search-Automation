def build_match_result(job, profile, score, risk_result):
    job_skills = {
        skill.lower()
        for skill in job.get("skills", [])
    }

    profile_skills = {
        skill.lower()
        for skill in (
            profile["core_skills"] +
            profile["additional_skills"]
        )
    }

    matched_skills = sorted(
        skill for skill in profile_skills
        if skill in job_skills
    )

    required_skills = [
        skill.strip()
        for skill in job.get("skills", [])
        if skill.strip()
    ]

    missing_skills = sorted(
        skill for skill in required_skills
        if skill.lower() not in profile_skills
    )

    risk = risk_result.get("risk", "UNKNOWN")
    risk_flags = risk_result.get("flags", [])

    if risk == "HIGH":
        recommendation = "DO NOT APPLY"
    elif score >= 90:
        recommendation = "APPLY"
    elif score >= 80:
        recommendation = "STRONG MATCH"
    elif score >= 70:
        recommendation = "REVIEW"
    else:
        recommendation = "SKIP"

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "risk": risk,
        "risk_flags": risk_flags,
        "recommendation": recommendation
    }