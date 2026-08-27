import re


def check_experience_eligibility(job, profile):
    experience = str(
        job.get("experience", "")
    ).strip().lower()

    max_years = profile.get(
        "max_experience_years",
        2
    )

    if not experience:
        return {
            "eligible": False,
            "status": "UNKNOWN",
            "reason": "EXPERIENCE NOT PROVIDED"
        }

    if (
        "fresher" in experience
        or "entry level" in experience
    ):
        return {
            "eligible": True,
            "status": "COMPATIBLE",
            "reason": "FRESHER / ENTRY LEVEL"
        }

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*years?",
        experience
    )

    if range_match:
        minimum = float(
            range_match.group(1)
        )
        maximum = float(
            range_match.group(2)
        )

        if maximum <= max_years:
            return {
                "eligible": True,
                "status": "COMPATIBLE",
                "reason": f"EXPERIENCE WITHIN {max_years} YEARS"
            }

        return {
            "eligible": False,
            "status": "INCOMPATIBLE",
            "reason": f"REQUIRES {minimum}-{maximum} YEARS"
        }

    single_match = re.search(
        r"(\d+(?:\.\d+)?)\+?\s*years?",
        experience
    )

    if single_match:
        years = float(
            single_match.group(1)
        )

        if years <= max_years:
            return {
                "eligible": True,
                "status": "COMPATIBLE",
                "reason": f"EXPERIENCE WITHIN {max_years} YEARS"
            }

        return {
            "eligible": False,
            "status": "INCOMPATIBLE",
            "reason": f"REQUIRES {years}+ YEARS"
        }

    return {
        "eligible": False,
        "status": "UNKNOWN",
        "reason": "EXPERIENCE COULD NOT BE DETERMINED"
    }