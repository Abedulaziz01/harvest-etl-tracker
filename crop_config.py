from dotenv import load_dotenv

load_dotenv()

CROP_CONFIG = {
    "maize": {
        "temp_min": 20,
        "temp_max": 30,
        "max_rain": 2,
        "humidity_min": 50,
        "humidity_max": 70,
        "points_temp": 40,
        "points_rain": 30,
        "points_humidity": 30,
        "description": "Maize in East Africa should usually be harvested during warm, relatively dry conditions so cobs can dry properly and avoid mold damage.",
    },
    "wheat": {
        "temp_min": 15,
        "temp_max": 25,
        "max_rain": 1,
        "humidity_min": 30,
        "humidity_max": 60,
        "points_temp": 40,
        "points_rain": 30,
        "points_humidity": 30,
        "description": "Wheat harvest is best in cool to mild, low-rain conditions with lower humidity to reduce grain moisture and post-harvest losses.",
    },
    "rice": {
        "temp_min": 25,
        "temp_max": 35,
        "max_rain": 5,
        "humidity_min": 60,
        "humidity_max": 80,
        "points_temp": 40,
        "points_rain": 30,
        "points_humidity": 30,
        "description": "Rice near harvest can tolerate warmer and more humid conditions, but excessive rain still increases drying difficulty and grain quality risks.",
    },
    "coffee": {
        "temp_min": 18,
        "temp_max": 24,
        "max_rain": 3,
        "humidity_min": 40,
        "humidity_max": 65,
        "points_temp": 40,
        "points_rain": 30,
        "points_humidity": 30,
        "description": "Coffee cherries should be harvested in mild temperatures with limited rainfall and moderate humidity to protect bean quality and drying conditions.",
    },
    "sorghum": {
        "temp_min": 25,
        "temp_max": 35,
        "max_rain": 2,
        "humidity_min": 30,
        "humidity_max": 60,
        "points_temp": 40,
        "points_rain": 30,
        "points_humidity": 30,
        "description": "Sorghum performs best for harvest in warm, dry weather with lower humidity so heads dry down well and weather damage is minimized.",
    },
}


if __name__ == "__main__":
    for crop_name, rules in CROP_CONFIG.items():
        print(f"{crop_name}: {rules}")
