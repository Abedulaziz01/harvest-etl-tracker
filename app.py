from pathlib import Path
import json
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from crop_config import CROP_CONFIG
from pipeline import run_pipeline

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "outputs" / "weekly_scores.csv"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"


def load_history():
    if CSV_PATH.exists():
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()


def load_latest_report():
    reports = sorted(REPORTS_DIR.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not reports:
        return None, None

    latest = reports[0]
    return latest, json.loads(latest.read_text(encoding="utf-8"))


st.set_page_config(
    page_title="Harvest Readiness Tracker",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(227, 188, 107, 0.22), transparent 28%),
            radial-gradient(circle at top left, rgba(104, 143, 90, 0.18), transparent 26%),
            linear-gradient(180deg, #f7f1df 0%, #efe7cf 46%, #e7dcc0 100%);
        color: #2f3327;
    }
    .hero {
        padding: 1.35rem 1.5rem;
        border-radius: 26px;
        background: linear-gradient(135deg, #5a7a48 0%, #7c5b2f 100%);
        color: #fff8ea;
        box-shadow: 0 20px 42px rgba(89, 66, 28, 0.18);
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.2rem;
        letter-spacing: 0.01em;
    }
    .hero p {
        margin: 0.55rem 0 0;
        font-size: 1rem;
        color: rgba(255, 248, 234, 0.92);
    }
    .section-title {
        background: linear-gradient(135deg, #fcf7eb, #f2e6cb);
        color: #425336;
        border-radius: 18px;
        padding: 0.8rem 1rem;
        margin: 0 0 0.8rem 0;
        border: 1px solid rgba(88, 103, 58, 0.12);
        box-shadow: 0 12px 24px rgba(99, 81, 40, 0.08);
        font-weight: 700;
        font-size: 1.05rem;
    }
    .latest-result-card {
        background: linear-gradient(180deg, #fdf8ee 0%, #f4ecd8 100%);
        border: 1px solid rgba(95, 114, 61, 0.14);
        border-radius: 24px;
        padding: 1rem 1.1rem 1.1rem 1.1rem;
        box-shadow: 0 14px 30px rgba(101, 81, 43, 0.10);
        margin-bottom: 1rem;
    }
    .latest-result-card h3,
    .latest-result-card p,
    .latest-result-card div,
    .latest-placeholder {
        color: #2f3327;
    }
    .latest-placeholder {
        background: linear-gradient(135deg, #eef4df, #dde9c6);
        border: 1px solid rgba(90, 122, 72, 0.16);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        font-weight: 600;
        color: #37522d;
    }
    .result-banner {
        background: linear-gradient(135deg, #56753f, #7a9b59);
        color: #fffdf5;
        border-radius: 18px;
        padding: 1rem 1.1rem 1.05rem 1.1rem;
        margin: 0.4rem 0 1rem 0;
        border: 1px solid rgba(67, 92, 50, 0.18);
        box-shadow: 0 14px 28px rgba(86, 117, 63, 0.16);
    }
    .result-banner strong {
        color: #fffef8;
    }
    .result-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.8rem 0 1rem 0;
    }
    .result-stat {
        background: linear-gradient(135deg, #ffffff, #f4eedf);
        border: 1px solid rgba(110, 126, 79, 0.12);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: 0 10px 22px rgba(92, 75, 39, 0.08);
    }
    .result-stat-label {
        color: #6b7158;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
    }
    .result-stat-value {
        color: #2f3327;
        font-size: 1.35rem;
        font-weight: 700;
    }
    .result-detail {
        background: linear-gradient(135deg, #fffdfa, #f6efdf);
        border: 1px solid rgba(104, 123, 70, 0.12);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        color: #33402d;
        margin-top: 0.9rem;
        box-shadow: 0 10px 22px rgba(92, 75, 39, 0.08);
    }
    .result-detail-title {
        color: #56683e;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }
    .report-card {
        background: linear-gradient(180deg, #fdf8ee 0%, #f4ecd8 100%);
        border: 1px solid rgba(95, 114, 61, 0.14);
        border-radius: 24px;
        padding: 1rem;
        box-shadow: 0 14px 30px rgba(101, 81, 43, 0.10);
    }
    .history-wrap {
        background: linear-gradient(180deg, #fdf8ee 0%, #f4ecd8 100%);
        border: 1px solid rgba(95, 114, 61, 0.14);
        border-radius: 22px;
        padding: 1rem;
        box-shadow: 0 14px 28px rgba(101, 81, 43, 0.10);
    }
    .history-empty {
        background: linear-gradient(135deg, #eef4df, #dde9c6);
        color: #37522d;
        border-radius: 16px;
        padding: 0.9rem 1rem;
        border: 1px solid rgba(90, 122, 72, 0.16);
    }
    </style>
    <div class="hero">
        <h1>Harvest Readiness Tracker</h1>
        <p>Run the ETL pipeline with one click, compare crop readiness, and review saved weekly advice.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

default_city = os.getenv("CITY", "Addis Ababa")
default_lat = os.getenv("LATITUDE", "9.0320")
default_lon = os.getenv("LONGITUDE", "38.7469")
default_crop = os.getenv("CROP", "maize").lower()

with st.sidebar:
    st.header("Run Settings")
    city = st.text_input("City", value=default_city)
    latitude = st.text_input("Latitude", value=default_lat)
    longitude = st.text_input("Longitude", value=default_lon)
    crop = st.selectbox("Crop", options=list(CROP_CONFIG.keys()), index=list(CROP_CONFIG.keys()).index(default_crop) if default_crop in CROP_CONFIG else 0)

    selected_rules = CROP_CONFIG[crop]
    st.caption("Current crop rules")
    st.write(
        {
            "temp_range_c": f"{selected_rules['temp_min']} - {selected_rules['temp_max']}",
            "max_rain_mm": selected_rules["max_rain"],
            "humidity_range_pct": f"{selected_rules['humidity_min']} - {selected_rules['humidity_max']}",
        }
    )

    run_clicked = st.button("Run Harvest Check", use_container_width=True, type="primary")

left, right = st.columns([1.2, 0.8])

with left:
    st.markdown('<div class="section-title">Latest Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="latest-result-card">', unsafe_allow_html=True)

    if run_clicked:
        with st.spinner("Running the pipeline and collecting advice..."):
            try:
                result = run_pipeline(
                    city=city,
                    latitude=latitude,
                    longitude=longitude,
                    crop=crop,
                )
                st.session_state["latest_result"] = result
                st.success("Harvest check completed successfully.")
            except Exception as exc:
                st.error(f"Pipeline run failed: {exc}")

    latest_result = st.session_state.get("latest_result")
    if latest_result:
        st.markdown(
            f"""
            <div class="result-banner">
                <strong>Latest Result Ready</strong><br>
                {latest_result['crop'].upper()} for {latest_result['city']} scored
                {latest_result['score']}/100 with status:
                {latest_result['interpretation']}.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="result-grid">
                <div class="result-stat">
                    <div class="result-stat-label">Crop</div>
                    <div class="result-stat-value">{latest_result['crop'].upper()}</div>
                </div>
                <div class="result-stat">
                    <div class="result-stat-label">Score</div>
                    <div class="result-stat-value">{latest_result['score']}/100</div>
                </div>
                <div class="result-stat">
                    <div class="result-stat-label">Avg Temp</div>
                    <div class="result-stat-value">{latest_result['avg_temp']} C</div>
                </div>
                <div class="result-stat">
                    <div class="result-stat-label">Avg Rain</div>
                    <div class="result-stat-value">{latest_result['avg_rain']} mm</div>
                </div>
            </div>
            <div class="result-detail">
                <div class="result-detail-title">Interpretation</div>
                <div>{latest_result['interpretation']}</div>
            </div>
            <div class="result-detail">
                <div class="result-detail-title">Average Humidity</div>
                <div>{latest_result['avg_humidity']}%</div>
            </div>
            <div class="result-detail">
                <div class="result-detail-title">AI Advice</div>
                <div>{latest_result['advice']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"Saved report: {latest_result['report_path']}")
    else:
        st.markdown(
            '<div class="latest-placeholder">Run the harvest check to see a live score and advice here.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">Latest Saved Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    latest_report_path, latest_report = load_latest_report()
    if latest_report:
        st.write(
            {
                "week": latest_report["week"],
                "city": latest_report["city"],
                "crop": latest_report["crop"],
                "score": latest_report["score"],
                "interpretation": latest_report["interpretation"],
            }
        )
        st.json(latest_report, expanded=False)
        st.caption(f"File: {latest_report_path.name}")
    else:
        st.write("No JSON reports saved yet.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-title">Weekly History</div>', unsafe_allow_html=True)
st.markdown('<div class="history-wrap">', unsafe_allow_html=True)
history_df = load_history()
if history_df.empty:
    st.markdown('<div class="history-empty">No weekly scores saved yet.</div>', unsafe_allow_html=True)
else:
    st.dataframe(history_df.sort_values("run_timestamp", ascending=False), use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
