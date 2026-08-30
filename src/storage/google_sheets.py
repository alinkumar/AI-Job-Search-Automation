import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDENTIALS_FILE = "credentials/reflected-night-506918-m3-db7d66f54cf8.json"
SHEET_NAME = "AI Job Search Dashboard"


HEADERS = [
    "Date",
    "Source",
    "Company",
    "Role",
    "Location",
    "Work Mode",
    "Experience",
    "Skills",
    "Score",
    "Risk",
    "Quality",
    "Decision",
    "Job URL"
]


def get_sheet():
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(
        credentials
    )

    spreadsheet = client.open(
        SHEET_NAME
    )

    return spreadsheet.sheet1


def ensure_headers(sheet):
    current_headers = [
        str(value).strip()
        for value in sheet.row_values(1)
    ]

    if current_headers != HEADERS:
        sheet.update(
            "A1:M1",
            [HEADERS],
            value_input_option="USER_ENTERED"
        )


def test_connection():
    sheet = get_sheet()

    ensure_headers(sheet)

    sheet.update(
        "A2",
        [["CONNECTION TEST"]],
        value_input_option="USER_ENTERED"
    )

    return True


def normalize_url(url):
    return str(
        url or ""
    ).strip()


def get_existing_urls(sheet):
    all_values = sheet.get_all_values()

    if not all_values:
        return set()

    headers = [
        str(value).strip()
        for value in all_values[0]
    ]

    if "Job URL" not in headers:
        return set()

    url_index = headers.index(
        "Job URL"
    )

    existing_urls = set()

    for row in all_values[1:]:
        if len(row) <= url_index:
            continue

        url = normalize_url(
            row[url_index]
        )

        if url:
            existing_urls.add(url)

    return existing_urls


def build_row(result):
    job = result.get(
        "job",
        {}
    )

    decision = result.get(
        "decision",
        {}
    )

    decision_name = str(
        decision.get(
            "decision",
            ""
        )
    ).strip()

    if decision_name not in [
        "APPLY",
        "STRONG MATCH",
        "REVIEW",
        "CONSIDER"
    ]:
        return None

    job_url = normalize_url(
        job.get(
            "job_url",
            ""
        )
    )

    if not job_url:
        return None

    skills = job.get(
        "skills",
        []
    )

    if isinstance(skills, str):
        skills_text = skills
    else:
        skills_text = ", ".join(
            str(skill)
            for skill in skills
        )

    return [
        job.get(
            "posted_date",
            ""
        ),
        job.get(
            "source",
            ""
        ),
        job.get(
            "company",
            ""
        ),
        job.get(
            "role",
            ""
        ),
        job.get(
            "location",
            ""
        ),
        job.get(
            "work_mode",
            ""
        ),
        job.get(
            "experience",
            ""
        ),
        skills_text,
        decision.get(
            "match_score",
            ""
        ),
        decision.get(
            "risk",
            ""
        ),
        decision.get(
            "quality",
            ""
        ),
        decision_name,
        job_url
    ]


def append_jobs(results):
    sheet = get_sheet()

    ensure_headers(
        sheet
    )

    existing_urls = get_existing_urls(
        sheet
    )

    rows = []

    for result in results:
        row = build_row(
            result
        )

        if not row:
            continue

        job_url = normalize_url(
            row[12]
        )

        if job_url in existing_urls:
            continue

        rows.append(row)

        existing_urls.add(
            job_url
        )

    if not rows:
        return 0

    sheet.append_rows(
        rows,
        value_input_option="USER_ENTERED"
    )

    return len(rows)