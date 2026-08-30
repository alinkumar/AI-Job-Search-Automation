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

RESTRICTED_COUNTRIES = [
    r"\bunited states\b",
    r"\busa\b",
    r"\bu\.s\.\b",
    r"\bunited kingdom\b",
    r"\buk\b",
    r"\bcanada\b",
    r"\baustralia\b",
    r"\bgermany\b",
    r"\bfrance\b",
    r"\bspain\b",
    r"\bitaly\b",
    r"\bmexico\b"
]


def contains_india(text):
    text = str(text or "").lower()

    return any(
        re.search(
            rf"\b{re.escape(location)}\b",
            text,
            re.IGNORECASE
        )
        for location in INDIA_LOCATIONS
    )


def contains_restricted_country(text):
    text = str(text or "").lower()

    return any(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
        for pattern in RESTRICTED_COUNTRIES
    )


def check_location_eligibility(job):
    location = str(
        job.get("location", "")
    ).strip().lower()

    description = str(
        job.get("description", "")
    ).lower()

    combined = f"{location} {description}"

    if contains_india(location):
        return {
            "eligible": True,
            "status": "INDIA ELIGIBLE",
            "reason": "INDIA LOCATION"
        }

    if re.search(
        r"\bremote\s*-\s*india\b",
        combined,
        re.IGNORECASE
    ):
        return {
            "eligible": True,
            "status": "INDIA REMOTE ELIGIBLE",
            "reason": "REMOTE INDIA"
        }

    if re.search(
        r"\bindia\b.*\bremote\b|\bremote\b.*\bindia\b",
        combined,
        re.IGNORECASE
    ):
        return {
            "eligible": True,
            "status": "INDIA REMOTE ELIGIBLE",
            "reason": "INDIA + REMOTE"
        }

    if contains_restricted_country(location):
        return {
            "eligible": False,
            "status": "NOT INDIA ELIGIBLE",
            "reason": "RESTRICTED COUNTRY"
        }

    if re.search(
        r"\bremote\b",
        location,
        re.IGNORECASE
    ):
        return {
            "eligible": True,
            "status": "REMOTE LOCATION",
            "reason": "REMOTE - VERIFY INDIA ELIGIBILITY"
        }

    if re.search(
        r"\bworldwide\b|\bglobal\b|\banywhere\b",
        location,
        re.IGNORECASE
    ):
        return {
            "eligible": True,
            "status": "GLOBAL REMOTE",
            "reason": "GLOBAL LOCATION - VERIFY ELIGIBILITY"
        }

    if re.search(
        r"\bapac\b|\basia\b",
        location,
        re.IGNORECASE
    ):
        return {
            "eligible": True,
            "status": "ASIA/APAC",
            "reason": "REGIONAL REMOTE - VERIFY ELIGIBILITY"
        }

    return {
        "eligible": False,
        "status": "UNKNOWN LOCATION",
        "reason": "INDIA LOCATION NOT CONFIRMED"
    }