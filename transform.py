import os

from dotenv import load_dotenv
from groq import Groq

from crop_config import CROP_CONFIG

load_dotenv()

CITY = os.getenv("CITY")
CROP = os.getenv("CROP", "maize").lower()


def get_interpretation(score):
    if score >= 80:
        return "Excellent - harvest now"
    if score >= 60:
        return "Good - proceed with minor caution"
    if score >= 40:
        return "Fair - consider waiting"
    return "Poor - do not harvest this week"


def calculate_score(weather_data):
    print(f"Crop selected: {CROP}")
    print("Loading crop rules from crop_config.py...")

    if CROP not in CROP_CONFIG:
        print(f"ERROR: '{CROP}' not found in crop_config.py")
        print(f"Available crops: {list(CROP_CONFIG.keys())}")
        return None

    rules = CROP_CONFIG[CROP]
    temperatures = weather_data["temperatures"]
    rainfall = weather_data["rainfall"]
    humidity = weather_data["humidity"]

    avg_temp = sum(temperatures) / len(temperatures)
    avg_rain = sum(rainfall) / len(rainfall)
    avg_humidity = sum(humidity) / len(humidity)

    print("Calculating harvest readiness score...")

    score = 0

    if rules["temp_min"] <= avg_temp <= rules["temp_max"]:
        score += rules["points_temp"]

    if avg_rain <= rules["max_rain"]:
        score += rules["points_rain"]

    if rules["humidity_min"] <= avg_humidity <= rules["humidity_max"]:
        score += rules["points_humidity"]

    result = {
        "crop": CROP,
        "score": score,
        "interpretation": get_interpretation(score),
        "avg_temp": round(avg_temp, 1),
        "avg_rain": round(avg_rain, 1),
        "avg_humidity": round(avg_humidity, 1),
        "city": CITY,
    }

    print(f"Score: {score}/100")
    return result


def get_ai_advice(score_data):
    print("Getting crop-specific advice from Groq...")

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    rules = CROP_CONFIG[CROP]
    client = Groq(api_key=groq_api_key)

    prompt = f"""
You are an expert agricultural advisor for Ethiopian smallholder farmers.

Based on the weather data below, give 3-4 sentences of plain-language
harvest advice specific to {score_data['crop']} farming in Ethiopia.

Crop:                    {score_data['crop'].upper()}
Region:                  {score_data['city']}, Ethiopia
Harvest Readiness Score: {score_data['score']}/100
Status:                  {score_data['interpretation']}
Average Temperature:     {score_data['avg_temp']}C  (ideal: {rules['temp_min']}-{rules['temp_max']}C)
Average Daily Rainfall:  {score_data['avg_rain']}mm  (threshold: below {rules['max_rain']}mm)
Average Humidity:        {score_data['avg_humidity']}%  (ideal: {rules['humidity_min']}-{rules['humidity_max']}%)

Crop context: {rules['description']}

Tell the farmer specifically: when to harvest, what weather risks to watch for
this week, and how to store this crop properly. Use simple language.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
    )

    advice = response.choices[0].message.content.strip()
    return advice


def transform_weather(weather_data):
    score_data = calculate_score(weather_data)
    if not score_data:
        return None

    advice = get_ai_advice(score_data)
    score_data["advice"] = advice
    return score_data


if __name__ == "__main__":
    test_weather = {
        "city": CITY,
        "dates": [
            "2026-04-16",
            "2026-04-17",
            "2026-04-18",
            "2026-04-19",
            "2026-04-20",
            "2026-04-21",
            "2026-04-22",
        ],
        "temperatures": [22, 23, 21, 24, 22, 23, 22],
        "rainfall": [0.0, 0.5, 1.2, 0.0, 0.3, 0.8, 0.0],
        "humidity": [58, 61, 65, 57, 60, 63, 59],
    }

    score_data = transform_weather(test_weather)

    if score_data:
        print(f"\nAdvice: {score_data['advice']}")
        print("\n--- Transform Result ---")
        print(
            f"Crop: {score_data['crop']} | Score: {score_data['score']}/100 | "
            f"Temp: {score_data['avg_temp']}C | "
            f"Rain: {score_data['avg_rain']}mm | "
            f"Humidity: {score_data['avg_humidity']}%"
        )
        print(f"Status: {score_data['interpretation']}")
