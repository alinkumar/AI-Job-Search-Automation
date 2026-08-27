DECISION_RANK = {
    "APPLY": 1,
    "STRONG MATCH": 2,
    "REVIEW": 3,
    "SKIP": 4,
    "DO NOT APPLY": 5
}


def rank_results(results):
    return sorted(
        results,
        key=lambda item: (
            DECISION_RANK.get(
                item.get("decision", {}).get("decision"),
                99
            ),
            -item.get("decision", {}).get("match_score", 0),
            -item.get("quality", {}).get("quality_score", 0)
        )
    )