import re


def filter_location(job, allowed_locations):
    location = str(
        job.get("location", "")
    ).lower()

    return any(
        loc.lower() in location
        for loc in allowed_locations
    )


def filter_experience(job, max_years=2):
    experience = str(
        job.get("experience", "")
    ).lower()

    blocked = [
        "3+ years",
        "4+ years",
        "5+ years",
        "6+ years",
        "7+ years",
        "8+ years",
        "senior",
        "lead",
        "manager",
        "principal",
        "director",
        "head"
    ]

    return not any(
        term in experience
        for term in blocked
    )


def filter_role(job, target_roles):
    role = str(
        job.get("role", "")
    ).strip().lower()

    blocked_roles = [
        "senior",
        "lead",
        "manager",
        "principal",
        "director",
        "head",
        "architect",
        "vp",
        "vice president"
    ]

    if any(
        re.search(
            rf"\b{re.escape(term)}\b",
            role
        )
        for term in blocked_roles
    ):
        return False

    role_patterns = [
        r"\bdata\s+analyst\b",
        r"\bjunior\s+data\s+analyst\b",
        r"\bdata\s+analyst\s+intern\b",
        r"\bdata\s+analytics?\s+intern\b",
        r"\bdata\s+science\s+intern\b",
        r"\bdata\s+analytics?\s+analyst\b",
        r"\banalytics?\s+analyst\b",
        r"\banalytics?\s+associate\b",
        r"\bbi\s+analyst\b",
        r"\bbusiness\s+intelligence\s+analyst\b",
        r"\breporting\s+analyst\b",
        r"\bdata\s+reporting\s+analyst\b",
        r"\banalytics?\s+reporting\b",
        r"\bmis\s+analyst\b",
        r"\bmis\s+executive\b",
        r"\bbusiness\s+data\s+analyst\b"
    ]

    if any(
        re.search(
            pattern,
            role,
            re.IGNORECASE
        )
        for pattern in role_patterns
    ):
        return True

    normalized_targets = [
        target.strip().lower()
        for target in target_roles
    ]

    return any(
        target in role
        for target in normalized_targets
    )