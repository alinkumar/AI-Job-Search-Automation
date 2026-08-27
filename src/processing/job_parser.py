import re

SKILL_PATTERNS = {
    "SQL": r"\bsql\b",
    "Microsoft Excel": r"\b(?:excel|microsoft excel|ms excel)\b",
    "Power BI": r"\bpower\s*bi\b",
    "Python": r"\bpython\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Data Cleaning": r"\bdata cleaning\b",
    "Exploratory Data Analysis": r"\b(?:exploratory data analysis|eda)\b",
    "Statistical Analysis": r"\b(?:statistical analysis|statistics)\b",
    "Data Visualization": r"\bdata visualization\b",
    "Feature Engineering": r"\bfeature engineering\b",
    "MySQL": r"\bmysql\b",
    "Machine Learning": r"\b(?:machine learning|ml)\b",
    "Deep Learning": r"\b(?:deep learning|dl)\b",
    "Scikit-learn": r"\b(?:scikit[\s-]?learn|sklearn)\b",
    "XGBoost": r"\bxgboost\b",
    "Git": r"\bgit\b",
    "GitHub": r"\bgithub\b",
    "Matplotlib": r"\bmatplotlib\b",
    "Seaborn": r"\bseaborn\b",
    "Plotly": r"\bplotly\b"
}


def extract_skills(description):
    text = str(description or "").lower()
    skills = []

    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            skills.append(skill)

    return skills


def format_number(value):
    number = float(value)
    return str(int(number)) if number.is_integer() else str(number)


def extract_experience(description):
    text = str(description or "").lower()

    structured_patterns = [
        r"experience\s*:\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"experience\s*:\s*(\d+(?:\.\d+)?)\s*(?:to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"experience\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"
    ]

    for pattern in structured_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            if match.lastindex == 2:
                return f"{format_number(match.group(1))}-{format_number(match.group(2))} years"

            value = format_number(match.group(1))

            if "+" in match.group(0):
                return f"{value}+ years"

            return f"{value} years"

    range_patterns = [
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*(?:to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)"
    ]

    for pattern in range_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return f"{format_number(match.group(1))}-{format_number(match.group(2))} years"

    fresher_terms = [
        "fresher",
        "freshers",
        "entry level",
        "entry-level",
        "no experience"
    ]

    if any(term in text for term in fresher_terms):
        return "Fresher / Entry Level"

    single_pattern = r"(\d+(?:\.\d+)?\+?)\s*(?:years?|yrs?)\s*(?:of)?\s*experience"

    match = re.search(single_pattern, text, re.IGNORECASE)

    if match:
        value = match.group(1)

        if value.endswith("+"):
            return f"{format_number(value[:-1])}+ years"

        return f"{format_number(value)} years"

    return "Unknown"


def extract_eligibility(description):
    text = str(description or "").lower()

    education_terms = [
        "b.sc",
        "bsc",
        "b.tech",
        "btech",
        "b.com",
        "bcom",
        "bachelor",
        "graduate",
        "graduation",
        "degree"
    ]

    if any(term in text for term in education_terms):
        return "Education requirement mentioned"

    if "students can apply" in text:
        return "Students eligible"

    if "freshers welcome" in text:
        return "Freshers eligible"

    return "Verify required"


def parse_job_description(description):
    return {
        "skills": extract_skills(description),
        "experience": extract_experience(description),
        "eligibility": extract_eligibility(description)
    }