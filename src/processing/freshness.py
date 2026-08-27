from datetime import datetime, timezone


def calculate_job_age_hours(posted_date):
    if not posted_date:
        return None

    try:
        posted = datetime.fromisoformat(
            posted_date.replace("Z", "+00:00")
        )

        if posted.tzinfo is None:
            posted = posted.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        age_hours = (now - posted).total_seconds() / 3600

        return max(age_hours, 0)

    except (ValueError, TypeError):
        return None


def check_freshness(posted_date, max_age_days=7):
    age_hours = calculate_job_age_hours(posted_date)

    if age_hours is None:
        return {
            "fresh": False,
            "age_hours": None,
            "age_days": None,
            "status": "VERIFY REQUIRED"
        }

    age_days = age_hours / 24

    if age_hours <= 24:
        status = "TODAY / VERY FRESH"
    elif age_hours <= 48:
        status = "FRESH"
    elif age_hours <= max_age_days * 24:
        status = "RECENT"
    else:
        status = "OLD"

    return {
        "fresh": age_hours <= max_age_days * 24,
        "age_hours": round(age_hours, 2),
        "age_days": round(age_days, 2),
        "status": status
    }