# Harvest Readiness Tracker

Harvest Readiness Tracker is a crop-aware ETL project for smallholder farming use cases in Ethiopia and East Africa. It collects 7-day weather data, scores harvest readiness using crop-specific rules, generates plain-language farming advice with Groq, saves weekly reports, and exposes the workflow through a Streamlit app.

## What The Project Does

- extracts 7-day forecast data from Open-Meteo
- transforms weather into a harvest readiness score out of 100
- uses crop-specific scoring rules for `maize`, `wheat`, `rice`, `coffee`, and `sorghum`
- generates crop-aware advice with Groq AI
- loads results into a CSV history file and weekly JSON reports
- supports automated scheduled runs every Monday at `06:00`
- provides a Streamlit interface for running the pipeline visually

## Project Structure

```text
harvest-etl-tracker/
├── .env
├── .gitignore
├── app.py
├── crop_config.py
├── extract.py
├── load.py
├── pipeline.py
├── scheduler.py
├── transform.py
├── outputs/
│   ├── weekly_scores.csv
│   ├── logs/
│   │   └── pipeline.log
│   └── reports/
│       └── 2026-W16_maize.json
└── venv/
```

## How It Works

### 1. Extract

`extract.py` reads `CITY`, `LATITUDE`, and `LONGITUDE`, then fetches:

- max temperature
- precipitation
- max humidity
- 7 daily timestamps

Source: Open-Meteo forecast API

### 2. Transform

`transform.py` reads the chosen crop, loads its rules from `crop_config.py`, and:

- averages temperature, rainfall, and humidity across 7 days
- scores harvest readiness based on crop thresholds
- maps the score to a simple interpretation
- sends the result to Groq for practical farming advice

### 3. Load

`load.py` saves:

- a new row to `outputs/weekly_scores.csv`
- a weekly crop-specific JSON report to `outputs/reports/`

### 4. Pipeline

`pipeline.py` runs all ETL steps in order:

1. extract weather
2. transform into score and advice
3. load into CSV and JSON outputs

It also writes run logs to `outputs/logs/pipeline.log`.

### 5. Scheduler

`scheduler.py` runs the pipeline:

- once immediately on startup
- every Monday at `06:00`

### 6. Streamlit App

`app.py` provides a simple interface where you can:

- choose a crop
- enter city and coordinates
- run the harvest check
- view the latest result
- view saved JSON reports
- review weekly CSV history

## Crop Rules

The crop scoring rules live in `crop_config.py`.

Each crop includes:

- ideal temperature range
- maximum average daily rainfall
- ideal humidity range
- scoring weights
- crop description used in the AI prompt

Supported crops:

- `maize`
- `wheat`
- `rice`
- `coffee`
- `sorghum`

## Environment Variables

Create a `.env` file in the project root with values like:

```env
GROQ_API_KEY=your_groq_api_key
CITY=Addis Ababa
LATITUDE=9.0320
LONGITUDE=38.7469
CROP=maize
```

Notes:

- `GROQ_API_KEY` is required for AI advice
- Open-Meteo does not require an API key
- `CROP` must match one of the keys in `crop_config.py`

## Installation

### 1. Create And Activate A Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install requests schedule pandas python-dotenv groq streamlit
```

## How To Run

### Run The Extract Step

```powershell
.\venv\Scripts\python extract.py
```

### Run The Transform Step

```powershell
.\venv\Scripts\python transform.py
```

### Run The Load Step

```powershell
.\venv\Scripts\python load.py
```

### Run The Full Pipeline

```powershell
.\venv\Scripts\python pipeline.py
```

### Run The Scheduler

```powershell
.\venv\Scripts\python scheduler.py
```

### Run The Streamlit App

```powershell
.\venv\Scripts\streamlit run app.py
```

## Output Files

### `outputs/weekly_scores.csv`

Stores one row per pipeline run, including:

- timestamp
- week
- city
- crop
- score
- interpretation
- average weather values
- AI advice

### `outputs/reports/*.json`

Stores one detailed JSON file per week and crop, including:

- score
- interpretation
- crop
- city
- weather summary
- advice

### `outputs/logs/pipeline.log`

Stores timestamped pipeline run logs.

## Verification Checklist

You know the project is working when:

- `extract.py` prints 7 days of weather
- `transform.py` returns a valid score and advice
- `load.py` creates a CSV row and JSON report
- `pipeline.py` completes all 3 stages
- `scheduler.py` starts and waits for the next scheduled run
- `app.py` opens in Streamlit and displays the latest results clearly

## Current Stack

- Python
- Open-Meteo
- Groq
- pandas
- schedule
- python-dotenv
- Streamlit

## Future Improvements

- make scheduler time configurable from the UI
- allow choosing multiple locations
- compare crops side by side
- add charts for score history
- export reports from Streamlit
- add deployment for shared access
