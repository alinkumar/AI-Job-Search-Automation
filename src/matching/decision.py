def make_final_decision(
    match_result,
    quality_result
):
    score = match_result.get(
        "score",
        0
    )

    risk = match_result.get(
        "risk",
        "UNKNOWN"
    )

    quality = quality_result.get(
        "quality",
        "LOW"
    )

    if risk == "HIGH":
        decision = "DO NOT APPLY"

    elif (
        score >= 90
        and quality == "HIGH"
    ):
        decision = "APPLY"

    elif (
        score >= 80
        and quality in [
            "HIGH",
            "MEDIUM"
        ]
    ):
        decision = "STRONG MATCH"

    elif (
        score >= 70
        and quality in [
            "HIGH",
            "MEDIUM"
        ]
    ):
        decision = "REVIEW"

    elif (
        score >= 55
        and quality in [
            "HIGH",
            "MEDIUM"
        ]
    ):
        decision = "CONSIDER"

    else:
        decision = "SKIP"

    return {
        "decision": decision,
        "match_score": score,
        "risk": risk,
        "quality": quality
    }