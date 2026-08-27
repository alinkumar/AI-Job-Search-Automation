CORE_SKILL_WEIGHTS = {
    "sql": 10,
    "microsoft excel": 8,
    "power bi": 8,
    "python": 7,
    "pandas": 5,
    "exploratory data analysis": 4,
    "statistical analysis": 4,
    "data cleaning": 4,
    "numpy": 2,
    "data visualization": 2,
    "feature engineering": 1,
    "mysql": 1
}

ROLE_WEIGHTS = {
    "data analyst": 25,
    "data analyst intern": 25,
    "junior data analyst": 25,
    "data analytics intern": 25,
    "data science intern": 20,
    "bi analyst": 18,
    "reporting analyst": 16,
    "mis analyst": 15,
    "analytics associate": 15
}


def calculate_match_score(job, profile):
    role = job.get("role", "").lower()
    job_skills = {
        skill.lower()
        for skill in job.get("skills", [])
    }

    score = 0

    role_score = 0

    for target_role, weight in ROLE_WEIGHTS.items():
        if target_role in role:
            role_score = max(role_score, weight)

    score += role_score

    matched_core_skills = []
    skill_score = 0

    for skill, weight in CORE_SKILL_WEIGHTS.items():
        if skill in job_skills:
            matched_core_skills.append(skill)
            skill_score += weight

    score += min(skill_score, 35)

    additional_skills = {
        skill.lower()
        for skill in profile["additional_skills"]
    }

    additional_matches = job_skills & additional_skills
    score += min(len(additional_matches) * 2, 10)

    experience = job.get("experience", "").lower()

    if any(term in experience for term in [
        "fresher",
        "entry level",
        "intern",
        "internship",
        "0-1",
        "0-2",
        "2 years"
    ]):
        score += 15

    location = job.get("location", "").lower()

    preferred_locations = {
        location_name.lower()
        for location_name in profile["preferred_locations"]
    }

    if any(location_name in location for location_name in preferred_locations):
        score += 10

    return min(score, 100)