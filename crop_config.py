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
        "description": "Maize is a staple grain crop in Ethiopia requiring warm dry conditions at harvest time.",
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
        "description": "Wheat is a cool-season grain that needs dry low-humidity conditions to avoid fungal disease at harvest.",
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
        "description": "Rice is a warm-season crop that tolerates higher humidity but needs rain to stop before harvest.",
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
        "description": "Ethiopian coffee requires mild temperatures and moderate dry conditions for quality cherry harvest.",
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
        "description": "Sorghum is a drought-tolerant grain that needs hot dry weather at harvest to prevent mold and rot.",
    },
}


if __name__ == "__main__":
    print("=== CROP CONFIG LOADED ===\n")
    for crop, rules in CROP_CONFIG.items():
        print(f"Crop:        {crop.upper()}")
        print(f"  Temp:      {rules['temp_min']}C - {rules['temp_max']}C")
        print(f"  Max Rain:  {rules['max_rain']}mm/day")
        print(f"  Humidity:  {rules['humidity_min']}% - {rules['humidity_max']}%")
        print(
            f"  Points:    temp={rules['points_temp']} "
            f"rain={rules['points_rain']} humidity={rules['points_humidity']}"
        )
        print()
