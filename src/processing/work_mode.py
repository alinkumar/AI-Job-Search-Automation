import re


REMOTE_PATTERNS = [
    r"\bremote\b",
    r"\bwork\s+from\s+home\b",
    r"\bwfh\b",
    r"\bfully\s+remote\b",
    r"\bremote\s+work\b"
]

HYBRID_PATTERNS = [
    r"\bhybrid\b",
    r"\bhybrid\s+work\b",
    r"\bhybrid\s+role\b",
    r"\bhybrid\s+model\b"
]

ONSITE_PATTERNS = [
    r"\bon[-\s]?site\b",
    r"\bin[-\s]?office\b",
    r"\bwork\s+from\s+office\b",
    r"\boffice[-\s]?based\b"
]


def contains_pattern(text, patterns):
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in patterns
    )


def detect_work_mode(job):
    title = str(job.get("role", ""))
    location = str(job.get("location", ""))
    description = str(job.get("description", ""))

    text = f"{title} {location} {description}"

    if contains_pattern(text, HYBRID_PATTERNS):
        return "Hybrid"

    if contains_pattern(text, REMOTE_PATTERNS):
        return "Remote"

    if contains_pattern(text, ONSITE_PATTERNS):
        return "On-site"

    return "Unknown"