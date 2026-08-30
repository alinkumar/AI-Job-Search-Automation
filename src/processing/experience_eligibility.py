import re


def check_experience_eligibility(job, profile):
    experience = str(
        job.get("experience", "")
    ).strip().lower()

    max_years = float(
        profile.get(
            "max_experience_years",
            2
        )
    )

    if not experience or experience == "unknown":
        return {
            "eligible": True,
            "status": "UNKNOWN",
            "reason": "EXPERIENCE NOT PROVIDED - MANUAL REVIEW"
        }

    if any(
        term in experience
        for term in [
            "fresher",
            "freshers",
            "entry level",
            "entry-level",
            "intern",
            "internship"
        ]
    ):
        return {
            "eligible": True,
            "status": "COMPATIBLE",
            "reason": "FRESHER / ENTRY LEVEL / INTERNSHIP"
        }

    plus_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+\s*years?",
        experience
    )

    if plus_match:
        years = float(
            plus_match.group(1)
        )

        if years <= 1:
            return {
                "eligible": True,
                "status": "COMPATIBLE",
                "reason": f"REQUIRES {years:g}+ YEARS"
            }

        return {
            "eligible": False,
            "status": "INCOMPATIBLE",
            "reason": f"REQUIRES {years:g}+ YEARS"
        }

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*years?",
        experience
    )

    if range_match:
        minimum = float(
            range_match.group(1)
        )

        maximum = float(
            range_match.group(2)
        )

        if minimum <= 1:
            return {
                "eligible": True,
                "status": "COMPATIBLE",
                "reason": (
                    f"REQUIRES {minimum:g}-{maximum:g} YEARS"
                )
            }

        if minimum <= max_years:
            return {
                "eligible": True,
                "status": "REVIEW",
                "reason": (
                    f"REQUIRES {minimum:g}-{maximum:g} YEARS"
                )
            }

        return {
            "eligible": False,
            "status": "INCOMPATIBLE",
            "reason": (
                f"REQUIRES {minimum:g}-{maximum:g} YEARS"
            )
        }

    single_match = re.search(
        r"(\d+(?:\.\d+)?)\s*years?",
        experience
    )

    if single_match:
        years = float(
            single_match.group(1)
        )

        if years <= 1:
            return {
                "eligible": True,
                "status": "COMPATIBLE",
                "reason": f"REQUIRES {years:g} YEARS"
            }

        if years <= max_years:
            return {
                "eligible": True,
                "status": "REVIEW",
                "reason": f"REQUIRES {years:g} YEARS"
            }

        return {
            "eligible": False,
            "status": "INCOMPATIBLE",
            "reason": f"REQUIRES {years:g} YEARS"
        }

    return {
        "eligible": True,
        "status": "UNKNOWN",
        "reason": "EXPERIENCE COULD NOT BE DETERMINED - MANUAL REVIEW"
    }