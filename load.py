import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
LOGS_DIR = OUTPUTS_DIR / "logs"
CSV_PATH = OUTPUTS_DIR / "weekly_scores.csv"


def get_report_label(score):
    if score >= 80:
        return "Excellent - ideal time to harvest"
    if score >= 60:
        return "Good - harvest possible with minor caution"
    if score >= 40:
        return "Fair - consider waiting or take precautions"
    return "Poor - not recommended to harvest this week"


def save_results(result_data):
    OUTPUTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    now = datetime.now()
    iso_year, iso_week, _ = now.isocalendar()
    week_name = f"{iso_year}-W{iso_week:02d}"
    crop = result_data["crop"]
    interpretation = get_report_label(result_data["score"])

    csv_row = {
        "run_timestamp": now.isoformat(timespec="seconds"),
        "week": week_name,
        "city": result_data["city"],
        "crop": crop,
        "score": result_data["score"],
        "interpretation": interpretation,
        "avg_temp": result_data["avg_temp"],
        "avg_rain": result_data["avg_rain"],
        "avg_humidity": result_data["avg_humidity"],
        "advice": result_data["advice"],
    }

    if CSV_PATH.exists():
        existing = pd.read_csv(CSV_PATH)
        updated = pd.concat([existing, pd.DataFrame([csv_row])], ignore_index=True)
    else:
        updated = pd.DataFrame([csv_row])

    updated.to_csv(CSV_PATH, index=False)

    report_data = {
        "generated_at": now.isoformat(timespec="seconds"),
        "week": week_name,
        "city": result_data["city"],
        "crop": crop,
        "score": result_data["score"],
        "interpretation": interpretation,
        "weather_summary": {
            "avg_temp": result_data["avg_temp"],
            "avg_rain": result_data["avg_rain"],
            "avg_humidity": result_data["avg_humidity"],
        },
        "advice": result_data["advice"],
    }

    report_path = REPORTS_DIR / f"{week_name}_{crop}.json"
    report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

    print(f"Scores saved to {CSV_PATH}")
    print(f"Report saved to {report_path}")

    return {
        "csv_path": str(CSV_PATH),
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    sample_result = {
        "city": "Addis Ababa",
        "crop": "maize",
        "score": 100,
        "avg_temp": 22.4,
        "avg_rain": 0.4,
        "avg_humidity": 60.4,
        "advice": (
            "Conditions are excellent for maize harvest this week. "
            "Harvest early while rainfall stays low and keep storage dry and ventilated."
        ),
    }

    save_results(sample_result)
