import os

import requests
from dotenv import load_dotenv

load_dotenv()

LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
CITY = os.getenv("CITY")


def fetch_weather():
    print(f"Fetching weather for {CITY}...")

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,precipitation_sum,relative_humidity_2m_max"
        f"&forecast_days=7"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        temperatures = data["daily"]["temperature_2m_max"]
        rainfall = data["daily"]["precipitation_sum"]
        humidity = data["daily"]["relative_humidity_2m_max"]
        dates = data["daily"]["time"]

        print("Weather data received successfully!")
        print("\n--- 7-Day Forecast ---")
        for i in range(7):
            print(
                f"Day {i+1} ({dates[i]}): Max Temp={temperatures[i]} C, "
                f"Rain={rainfall[i]}mm, Humidity={humidity[i]}%"
            )

        return {
            "city": CITY,
            "dates": dates,
            "temperatures": temperatures,
            "rainfall": rainfall,
            "humidity": humidity,
        }

    except requests.exceptions.ConnectionError:
        print("Connection Error - check your internet connection.")
        return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None


if __name__ == "__main__":
    fetch_weather()
