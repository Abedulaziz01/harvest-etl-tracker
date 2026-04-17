import os
import time
from datetime import datetime

import schedule
from dotenv import load_dotenv

from pipeline import run_pipeline

load_dotenv()


def job():
    print("\nRunning scheduled pipeline job...")
    run_pipeline()


def run_scheduler():
    crop = os.getenv("CROP", "maize").lower()
    city = os.getenv("CITY", "Unknown")
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 40)
    print("  HARVEST TRACKER SCHEDULER RUNNING")
    print(f"  Crop: {crop} | Region: {city}")
    print("  Runs every Monday at 06:00 AM")
    print(f"  Started: {started}")
    print("  Press Ctrl+C to stop")
    print("=" * 40)

    schedule.every().monday.at("06:00").do(job)

    print("\nRunning pipeline now for testing...")
    run_pipeline()

    print("\nScheduler waiting for next Monday 06:00 run...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
