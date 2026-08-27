import re


INDIA_LOCATIONS = [
    "india",
    "delhi",
    "new delhi",
    "noida",
    "gurgaon",
    "gurugram",
    "ghaziabad",
    "faridabad",
    "hyderabad",
    "mumbai",
    "bangalore",
    "bengaluru",
    "pune",
    "chennai",
    "kolkata",
    "jaipur",
    "ahmedabad"
]

US_PATTERNS = [
    r"\bremote\s*-\s*us\b",
    r"\bunited states\b",
    r"\busa\b",
    r"\bu\.s\.\b",
    r"\bmust reside in.*states\b",
    r"\bapproved states\b"
]


def is_india_location(location):
    location = str(location or "").lower()

    if any(
        re.search(pattern, location, re.IGNORECASE)
        for pattern in US_PATTERNS
    ):
        return False

    return any(
        india_location in location
        for india_location in INDIA_LOCATIONS
    )


def check_location_eligibility(job):
    location = str(job.get("location", "")).lower()
    description = str(job.get("description", "")).lower()

    combined = f"{location} {description}"

    if any(
        re.search(pattern, combined, re.IGNORECASE)
        for pattern in US_PATTERNS
    ):
        return {
            "eligible": False,
            "status": "NOT INDIA ELIGIBLE",
            "reason": "US LOCATION RESTRICTION"
        }

    if is_india_location(location):
        return {
            "eligible": True,
            "status": "INDIA ELIGIBLE",
            "reason": "INDIA LOCATION"
        }

    if "remote" in combined:
        return {
            "eligible": False,
            "status": "UNKNOWN REMOTE ELIGIBILITY",
            "reason": "INDIA ELIGIBILITY NOT CONFIRMED"
        }

    return {
        "eligible": False,
        "status": "UNKNOWN LOCATION",
        "reason": "INDIA LOCATION NOT CONFIRMED"
    }