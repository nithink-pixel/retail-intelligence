# 📊 Real-Time Retail Price Intelligence Engine

> An automated pricing intelligence system that scrapes live product data, detects price anomalies, and surfaces insights through a live public dashboard — running continuously with zero manual intervention.

## 🔴 Live Dashboard
**[Open Live Dashboard →](https://nithin-retail-intelligence.streamlit.app)**

## What It Does
- Scrapes pricing data across 100+ products automatically every 6 hours
- Loads into a DuckDB warehouse via structured SQL transformations
- Detects price shifts greater than 5% and fires alerts
- Serves a live Streamlit dashboard with interactive filters, trend charts, and a price alert feed

## Architecture
cd ~/retail-intelligence
cat > README.md << 'EOF'
# 📊 Real-Time Retail Price Intelligence Engine

> An automated pricing intelligence system that scrapes live product data, detects price anomalies, and surfaces insights through a live public dashboard — running continuously with zero manual intervention.

## 🔴 Live Dashboard
**[Open Live Dashboard →](https://nithin-retail-intelligence.streamlit.app)**

## What It Does
- Scrapes pricing data across 100+ products automatically every 6 hours
- Loads into a DuckDB warehouse via structured SQL transformations
- Detects price shifts greater than 5% and fires alerts
- Serves a live Streamlit dashboard with interactive filters, trend charts, and a price alert feed

## Architecture
```
Web Sources → Python Scraper → DuckDB Warehouse → Anomaly Engine → Streamlit Dashboard
                                                          ↑
                                               GitHub Actions (every 6h)
```

## Tech Stack
| Layer | Tools |
|---|---|
| Scraping | Python, BeautifulSoup, Requests |
| Warehouse | DuckDB, SQL |
| Transformation | Pandas, SQL CTEs |
| Dashboard | Streamlit, Plotly |
| Automation | GitHub Actions |

## Key Features
- **Zero manual intervention** after setup — fully automated end to end
- **Anomaly detection** flags any product with price shift greater than 5%
- **Interactive dashboard** with rating filters, price range slider, and live alert feed
- **Production architecture** — same pattern used by retail pricing teams

## Project Structure
```
retail-intelligence/
├── scraper/
│   └── scrape_prices.py       # Web scraping pipeline
├── database/
│   ├── load_prices.py         # DuckDB loader + anomaly detection
│   └── schema.sql             # Table definitions
├── dashboard/
│   └── app.py                 # Streamlit dashboard
├── packages.txt               # System dependencies
├── requirements.txt           # Python dependencies
└── README.md
```

## Screenshots
Built and deployed in a single session. Live at:
**https://nithin-retail-intelligence.streamlit.app**
