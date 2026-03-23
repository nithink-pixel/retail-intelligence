# Real-Time Retail Price Intelligence Engine

An automated pricing intelligence system that scrapes live product data, detects price anomalies, and surfaces insights through a live dashboard — running continuously with zero manual intervention.

**Live Dashboard:** https://nithin-retail-intelligence.streamlit.app

## What it does
- Scrapes pricing data across 100+ products every 6 hours automatically
- Loads into a DuckDB warehouse via structured SQL transformations
- Detects price shifts greater than 5% and fires alerts
- Serves a live Streamlit dashboard with interactive filters and trend charts

## Stack
Python · DuckDB · SQL · Streamlit · Plotly · GitHub Actions · BeautifulSoup

## Architecture
Scraper (Python) → DuckDB warehouse → Anomaly detection engine → Live Streamlit dashboard
Scheduler: GitHub Actions runs the full pipeline every 6 hours automatically

## Project structure
```
retail-intelligence/
├── scraper/          # Web scraping pipeline
├── database/         # DuckDB warehouse + SQL transformations
├── dashboard/        # Streamlit app
└── .github/workflows # Automated scheduler
```
