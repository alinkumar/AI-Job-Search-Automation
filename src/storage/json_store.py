import json
from datetime import datetime, timezone
from pathlib import Path


def save_results(output):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    file_path = data_dir / f"jobs_{timestamp}.json"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    return file_path