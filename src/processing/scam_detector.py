import re


SUSPICIOUS_TERMS = [
    "registration fee",
    "processing fee",
    "security deposit",
    "training fee",
    "pay to apply",
    "pay before joining",
    "upi payment",
    "guaranteed job",
    "guaranteed placement"
]


NEGATION_PATTERNS = [
    r"\bno\s+(?:registration|application|processing|training)\s+fee\b",
    r"\bno\s+(?:security\s+deposit|upi\s+payment)\b",
    r"\bwithout\s+(?:registration|application|processing|training)\s+fee\b",
    r"\bwithout\s+(?:security\s+deposit|upi\s+payment)\b",
    r"\bnever\s+(?:pay|paying)\b",
    r"\bdo\s+not\s+(?:pay|make\s+a\s+payment)\b",
    r"\bdon['’]?t\s+(?:pay|make\s+a\s+payment)\b"
]


def is_negated(term, text):
    pattern = rf"\b(?:no|without|never|do not|don't|don’t)\s+(?:\w+\s+){{0,3}}{re.escape(term)}\b"

    if re.search(pattern, text, re.IGNORECASE):
        return True

    for pattern in NEGATION_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)

        if match and term in match.group(0):
            return True

    return False


def detect_scam_risk(job):
    text = " ".join([
        job.get("description", ""),
        job.get("eligibility", "")
    ]).lower()

    flags = []

    for term in SUSPICIOUS_TERMS:
        if term in text and not is_negated(term, text):
            flags.append(term)

    if flags:
        return {
            "risk": "HIGH",
            "flags": flags
        }

    return {
        "risk": "LOW",
        "flags": []
    }