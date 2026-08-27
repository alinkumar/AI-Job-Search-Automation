def filter_location(job, allowed_locations):
    location = job.get("location", "").lower()
    return any(loc.lower() in location for loc in allowed_locations)


def filter_experience(job, max_years=2):
    experience = job.get("experience", "").lower()

    blocked = [
        "3+ years",
        "4+ years",
        "5+ years",
        "6+ years",
        "7+ years",
        "8+ years",
        "senior",
        "lead",
        "manager"
    ]

    return not any(term in experience for term in blocked)


def filter_role(job, target_roles):
    role = job.get("role", "").lower()
    return any(target.lower() in role for target in target_roles)