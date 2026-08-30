from datetime import datetime
from src.processing.work_mode import detect_work_mode
from src.processing.job_parser import parse_job_description


def clean_value(value):
    if value is None:
        return ""

    if isinstance(value, (list, tuple)):
        return ", ".join(
            clean_value(item)
            for item in value
            if clean_value(item)
        )

    return str(value).strip()


def get_value(job, keys, default=""):
    if not isinstance(job, dict):
        return default

    for key in keys:
        value = job.get(key)

        if value not in [None, "", [], {}]:
            return value

    return default


def nested_value(job, paths, default=""):
    for path in paths:
        current = job

        try:
            for key in path:
                if isinstance(current, dict):
                    current = current.get(key)
                else:
                    current = None

            if current not in [None, "", [], {}]:
                return current
        except Exception:
            continue

    return default


def parse_date(value):
    if not value:
        return ""

    value = str(value).strip()

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        ).isoformat()
    except ValueError:
        pass

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                value,
                fmt
            ).isoformat()
        except ValueError:
            continue

    return ""


def extract_salary(job):
    salary_min = get_value(
        job,
        [
            "salary_min",
            "salary_minimum",
            "min_salary",
            "minimum_salary"
        ],
        0
    )

    salary_max = get_value(
        job,
        [
            "salary_max",
            "salary_maximum",
            "max_salary",
            "maximum_salary"
        ],
        0
    )

    try:
        salary_min = float(salary_min or 0)
    except (TypeError, ValueError):
        salary_min = 0

    try:
        salary_max = float(salary_max or 0)
    except (TypeError, ValueError):
        salary_max = 0

    if salary_min and salary_max:
        return f"₹{salary_min:,.0f} - ₹{salary_max:,.0f}"

    if salary_max:
        return f"Up to ₹{salary_max:,.0f}"

    if salary_min:
        return f"From ₹{salary_min:,.0f}"

    salary = get_value(
        job,
        [
            "salary",
            "salary_range",
            "compensation",
            "salary_description",
            "pay"
        ]
    )

    return clean_value(salary) or "Not disclosed"


def extract_company(job):
    company = get_value(
        job,
        [
            "company",
            "company_name",
            "employer",
            "employer_name",
            "organization",
            "organisation"
        ]
    )

    if isinstance(company, dict):
        company = get_value(
            company,
            [
                "display_name",
                "name",
                "title",
                "company_name"
            ]
        )

    if not company:
        company = nested_value(
            job,
            [
                ["company", "display_name"],
                ["company", "name"],
                ["employer", "name"],
                ["employer", "display_name"]
            ]
        )

    return clean_value(company)


def extract_location(job):
    location = get_value(
        job,
        [
            "location",
            "locations",
            "city",
            "place",
            "job_location",
            "workplace"
        ]
    )

    if isinstance(location, dict):
        location = get_value(
            location,
            [
                "display_name",
                "name",
                "city",
                "location",
                "address"
            ]
        )

    if isinstance(location, list):
        values = []

        for item in location:
            if isinstance(item, dict):
                value = get_value(
                    item,
                    [
                        "display_name",
                        "name",
                        "city",
                        "location"
                    ]
                )
            else:
                value = item

            if value:
                values.append(
                    clean_value(value)
                )

        location = ", ".join(values)

    if not location:
        location = nested_value(
            job,
            [
                ["location", "display_name"],
                ["location", "name"],
                ["location", "city"],
                ["job", "location"],
                ["job", "city"]
            ]
        )

    return clean_value(location)


def extract_description(job):
    description = get_value(
        job,
        [
            "description",
            "content",
            "job_description",
            "summary",
            "details",
            "snippet",
            "body",
            "job_details"
        ]
    )

    if isinstance(description, dict):
        description = get_value(
            description,
            [
                "text",
                "content",
                "description",
                "value"
            ]
        )

    return clean_value(description)


def extract_role(job):
    role = get_value(
        job,
        [
            "title",
            "role",
            "job_title",
            "position",
            "position_title",
            "job_name",
            "name"
        ]
    )

    if isinstance(role, dict):
        role = get_value(
            role,
            [
                "title",
                "name",
                "text"
            ]
        )

    return clean_value(role)


def extract_url(job):
    url = get_value(
        job,
        [
            "redirect_url",
            "url",
            "job_url",
            "apply_url",
            "link",
            "application_url",
            "apply_link",
            "job_link"
        ]
    )

    if isinstance(url, dict):
        url = get_value(
            url,
            [
                "url",
                "link",
                "href"
            ]
        )

    return clean_value(url)


def extract_job_id(job, source):
    job_id = get_value(
        job,
        [
            "id",
            "job_id",
            "guid",
            "uuid",
            "jobId",
            "jobID"
        ]
    )

    if isinstance(job_id, dict):
        job_id = get_value(
            job_id,
            [
                "id",
                "value"
            ]
        )

    if not job_id:
        job_id = extract_url(job)

    if not job_id:
        job_id = (
            extract_company(job)
            + "|"
            + extract_role(job)
            + "|"
            + extract_location(job)
        )

    if not job_id:
        return ""

    return (
        f"{source.lower().replace(' ', '_')}_"
        f"{clean_value(job_id)}"
    )


def extract_posted_date(job):
    value = get_value(
        job,
        [
            "created",
            "created_at",
            "posted_date",
            "published_at",
            "publication_date",
            "date",
            "published",
            "pubDate",
            "updated_at",
            "updated"
        ]
    )

    return parse_date(value)


def parse_description(description, role):
    if not description:
        return {
            "skills": [],
            "experience": "Unknown",
            "eligibility": "Verify required"
        }

    try:
        result = parse_job_description(
            description,
            role
        )
    except TypeError:
        result = parse_job_description(
            description
        )

    if not isinstance(result, dict):
        return {
            "skills": [],
            "experience": "Unknown",
            "eligibility": "Verify required"
        }

    return result


def transform_generic_job(job, source):
    description = extract_description(job)
    role = extract_role(job)
    location = extract_location(job)

    parsed = parse_description(
        description,
        role
    )

    return {
        "job_id": extract_job_id(
            job,
            source
        ),
        "source": source,
        "company": extract_company(job),
        "role": role,
        "location": location,
        "work_mode": detect_work_mode({
            "role": role,
            "location": location,
            "description": description
        }),
        "salary": extract_salary(job),
        "skills": parsed.get(
            "skills",
            []
        ),
        "description": description,
        "job_url": extract_url(job),
        "posted_date": extract_posted_date(job),
        "experience": parsed.get(
            "experience",
            "Unknown"
        ),
        "eligibility": parsed.get(
            "eligibility",
            "Verify required"
        )
    }


def transform_adzuna_job(job):
    return transform_generic_job(
        job,
        "Adzuna"
    )


def transform_muse_job(job):
    return transform_generic_job(
        job,
        "The Muse"
    )


def transform_jooble_job(job):
    return transform_generic_job(
        job,
        "Jooble"
    )


def transform_himalayas_job(job):
    return transform_generic_job(
        job,
        "Himalayas"
    )


def transform_jobicy_job(job):
    return transform_generic_job(
        job,
        "Jobicy"
    )


def transform_remotive_job(job):
    return transform_generic_job(
        job,
        "Remotive"
    )


def transform_job(job, source):
    transformers = {
        "Adzuna": transform_adzuna_job,
        "The Muse": transform_muse_job,
        "Jooble": transform_jooble_job,
        "Himalayas": transform_himalayas_job,
        "Jobicy": transform_jobicy_job,
        "Remotive": transform_remotive_job
    }

    transformer = transformers.get(
        source
    )

    if not transformer:
        raise ValueError(
            f"Unsupported source: {source}"
        )

    return transformer(job)