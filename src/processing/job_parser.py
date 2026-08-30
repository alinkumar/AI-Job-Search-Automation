import re


SKILL_PATTERNS = {
    "SQL": [
        r"\bsql\b",
        r"\bsql\s+server\b",
        r"\bms\s+sql\b",
        r"\bmssql\b"
    ],
    "Microsoft Excel": [
        r"\bexcel\b",
        r"\bmicrosoft\s+excel\b",
        r"\bms\s+excel\b",
        r"\bms\s+office\b"
    ],
    "Power BI": [
        r"\bpower\s*bi\b",
        r"\bpowerbi\b"
    ],
    "Python": [
        r"\bpython\b"
    ],
    "Pandas": [
        r"\bpandas\b"
    ],
    "NumPy": [
        r"\bnumpy\b"
    ],
    "MySQL": [
        r"\bmysql\b"
    ],
    "PostgreSQL": [
        r"\bpostgresql\b",
        r"\bpostgres\b"
    ],
    "Alteryx": [
        r"\balteryx\b"
    ],
    "Power Query": [
        r"\bpower\s+query\b",
        r"\bpowerquery\b"
    ],
    "Power Pivot": [
        r"\bpower\s+pivot\b",
        r"\bpowerpivot\b"
    ],
    "DAX": [
        r"\bdax\b"
    ],
    "Tableau": [
        r"\btableau\b"
    ],
    "Looker": [
        r"\blooker\b",
        r"\blooker\s+studio\b"
    ],
    "Data Cleaning": [
        r"\bdata\s+(?:cleaning|cleansing)\b",
        r"\bclean(?:ing)?\s+(?:datasets?|data)\b",
        r"\bdata\s+preparation\b"
    ],
    "Exploratory Data Analysis": [
        r"\bexploratory\s+data\s+analysis\b",
        r"\bexploratory\s+analysis\b",
        r"\beda\b"
    ],
    "Statistical Analysis": [
        r"\bstatistical\s+analysis\b",
        r"\bstatistical\s+analyses\b",
        r"\bstatistics\b",
        r"\bstatistical\s+methods?\b"
    ],
    "Data Visualization": [
        r"\bdata\s+(?:visualization|visualisation)\b",
        r"\bvisuali[sz](?:ation|ations|isation|isations)\b"
    ],
    "Feature Engineering": [
        r"\bfeature\s+engineering\b"
    ],
    "Business Intelligence": [
        r"\bbusiness\s+intelligence\b",
        r"\bbi\s+reporting\b"
    ],
    "Data Analysis": [
        r"\bdata\s+analysis\b",
        r"\banalytics\b"
    ],
    "Reporting": [
        r"\breporting\b",
        r"\breports?\b"
    ],
    "Dashboarding": [
        r"\bdashboard(?:s|ing)?\b"
    ],
    "ETL": [
        r"\betl\b",
        r"\bextract\s+transform\s+load\b"
    ],
    "KPI Reporting": [
        r"\bkpis?\b",
        r"\bkey\s+performance\s+indicators?\b"
    ],
    "Machine Learning": [
        r"\bmachine\s+learning\b",
        r"\bml\b"
    ],
    "Deep Learning": [
        r"\bdeep\s+learning\b",
        r"\bdl\b"
    ],
    "Scikit-learn": [
        r"\bscikit[\s-]?learn\b",
        r"\bsklearn\b"
    ],
    "XGBoost": [
        r"\bxgboost\b"
    ],
    "Matplotlib": [
        r"\bmatplotlib\b"
    ],
    "Seaborn": [
        r"\bseaborn\b"
    ],
    "Plotly": [
        r"\bplotly\b"
    ],
    "Git": [
        r"\bgit\b"
    ],
    "GitHub": [
        r"\bgithub\b"
    ]
}


def extract_skills(description):
    text = str(
        description or ""
    ).lower()

    skills = []

    for skill, patterns in SKILL_PATTERNS.items():
        for pattern in patterns:
            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):
                skills.append(skill)
                break

    return skills


def format_number(value):
    number = float(value)

    if number.is_integer():
        return str(int(number))

    return str(number)


def extract_experience(description, role=""):
    text = str(
        description or ""
    ).lower()

    role_text = str(
        role or ""
    ).lower()

    if re.search(
        r"\b(?:intern|internship)\b",
        role_text
    ):
        return "Fresher / Entry Level"

    if re.search(
        r"\b(?:fresher|freshers|entry[- ]level|intern|internship|no experience)\b",
        text
    ):
        return "Fresher / Entry Level"

    if re.search(
        r"\b0\s*(?:years?|yrs?)\s*(?:of)?\s*experience\b",
        text
    ):
        return "Fresher / Entry Level"

    range_patterns = [
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*(?:to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)"
    ]

    for pattern in range_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return (
                f"{format_number(match.group(1))}-"
                f"{format_number(match.group(2))} years"
            )

    plus_patterns = [
        r"(\d+(?:\.\d+)?)\+\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*\+"
    ]

    for pattern in plus_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return (
                f"{format_number(match.group(1))}+ years"
            )

    structured_patterns = [
        r"experience\s*:\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"experience\s*:\s*(\d+(?:\.\d+)?)\s*(?:to)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"experience\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"
    ]

    for pattern in structured_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            if match.lastindex == 2:
                return (
                    f"{format_number(match.group(1))}-"
                    f"{format_number(match.group(2))} years"
                )

            value = format_number(
                match.group(1)
            )

            if "+" in match.group(0):
                return f"{value}+ years"

            return f"{value} years"

    single_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:in|as|of)\s+[^.]{0,100}(?:role|position|experience)",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+in\s+(?:a\s+)?(?:data\s+analyst|analytics|data\s+science)"
    ]

    for pattern in single_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            value = match.group(1)

            if "+" in match.group(0):
                return f"{format_number(value)}+ years"

            return f"{format_number(value)} years"

    return "Unknown"


def extract_eligibility(description):
    text = str(
        description or ""
    ).lower()

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

    if "students can apply" in text:
        return "Students eligible"

    if "freshers welcome" in text:
        return "Freshers eligible"

    if any(
        term in text
        for term in education_terms
    ):
        return "Education requirement mentioned"

    return "Verify required"


def parse_job_description(
    description,
    role=""
):
    return {
        "skills": extract_skills(
            description
        ),
        "experience": extract_experience(
            description,
            role
        ),
        "eligibility": extract_eligibility(
            description
        )
    }