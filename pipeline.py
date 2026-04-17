import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from extract import fetch_weather
from load import save_results
from transform import transform_weather

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "outputs" / "logs"
LOG_FILE = LOGS_DIR / "pipeline.log"


def get_logger():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("harvest_tracker_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    return logger


def run_pipeline():
    logger = get_logger()

    crop = os.getenv("CROP", "maize").lower()
    city = os.getenv("CITY", "Unknown")
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 40)
    print("  HARVEST READINESS PIPELINE STARTING")
    print(f"  Crop: {crop} | City: {city}")
    print(f"  {started}")
    print("=" * 40)

    logger.info("Pipeline started | Crop: %s | City: %s", crop, city)

    print(f"\n[ 1/3 ] EXTRACT - Fetching 7-day weather for {city}...")
    weather_data = fetch_weather()
    if not weather_data:
        logger.error("Extract failed - no weather data returned")
        raise ValueError("Extract step failed - no weather data returned.")
    logger.info("Extract complete - 7 days of weather received")

    print(f"[ 2/3 ] TRANSFORM - Scoring {crop} + getting Groq advice...")
    transformed_data = transform_weather(weather_data)
    if not transformed_data:
        logger.error("Transform failed - no transformed data returned")
        raise ValueError("Transform step failed - no score data returned.")
    logger.info(
        "Transform complete - Crop: %s | Score: %s/100",
        transformed_data["crop"],
        transformed_data["score"],
    )

    print("[ 3/3 ] LOAD - Saving results to files...")
    saved_paths = save_results(transformed_data)
    logger.info("Load complete - files saved")
    logger.info("Pipeline complete")

    print("\n" + "=" * 40)
    print("  PIPELINE COMPLETE")
    print(f"  Crop: {transformed_data['crop']}")
    print(f"  Score this week: {transformed_data['score']}/100")
    print(f"  Status: {transformed_data['interpretation']}")
    print("=" * 40)

    return {
        "crop": transformed_data["crop"],
        "score": transformed_data["score"],
        "interpretation": transformed_data["interpretation"],
        "csv_path": saved_paths["csv_path"],
        "report_path": saved_paths["report_path"],
    }


if __name__ == "__main__":
    run_pipeline()
