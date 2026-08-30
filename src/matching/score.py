CORE_SKILL_WEIGHTS = {
    "sql": 12,
    "microsoft excel": 10,
    "power bi": 10,
    "python": 9,
    "pandas": 6,
    "exploratory data analysis": 5,
    "statistical analysis": 5,
    "data cleaning": 5,
    "data visualization": 4,
    "numpy": 3,
    "mysql": 3,
    "feature engineering": 2
}


ROLE_WEIGHTS = {
    "data analyst intern": 30,
    "data analytics intern": 30,
    "junior data analyst": 29,
    "data science intern": 27,
    "data analyst": 25,
    "bi analyst": 23,
    "reporting analyst": 21,
    "mis analyst": 20,
    "analytics associate": 20
}


def calculate_match_score(job, profile):
    role = str(
        job.get("role", "")
    ).lower().strip()

    job_skills = {
        str(skill).lower().strip()
        for skill in job.get("skills", [])
    }

    score = 0

    role_score = 0

    for target_role, weight in ROLE_WEIGHTS.items():
        if target_role in role:
            role_score = max(
                role_score,
                weight
            )

    score += role_score

    skill_score = 0

    for skill, weight in CORE_SKILL_WEIGHTS.items():
        if skill in job_skills:
            skill_score += weight

    score += min(
        skill_score,
        40
    )

    additional_skills = {
        str(skill).lower().strip()
        for skill in profile.get(
            "additional_skills",
            []
        )
    }

    additional_matches = (
        job_skills & additional_skills
    )

    score += min(
        len(additional_matches) * 2,
        8
    )

    experience = str(
        job.get("experience", "")
    ).lower().strip()

    if any(
        term in experience
        for term in [
            "fresher",
            "entry level",
            "entry-level",
            "intern",
            "internship"
        ]
    ):
        score += 20

    elif "0-1 years" in experience:
        score += 20

    elif "0-1 year" in experience:
        score += 20

    elif "1 year" in experience:
        score += 18

    elif "1+ year" in experience:
        score += 17

    elif "2 years" in experience:
        score += 10

    elif "2+ years" in experience:
        score += 8

    elif experience in [
        "",
        "unknown"
    ]:
        score += 5

    location = str(
        job.get("location", "")
    ).lower().strip()

    preferred_locations = {
        str(location_name).lower().strip()
        for location_name in profile.get(
            "preferred_locations",
            []
        )
    }

    if any(
        location_name in location
        for location_name in preferred_locations
    ):
        score += 10

    if any(
        term in location
        for term in [
            "delhi",
            "noida",
            "gurgaon",
            "gurugram"
        ]
    ):
        score += 2

    return min(
        score,
        100
    )