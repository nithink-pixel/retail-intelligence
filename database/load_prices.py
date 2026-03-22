import duckdb
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.scrape_prices import scrape_books

DB_PATH = "database/retail.db"

def setup_database(conn):
    """Creates the tables if they don't exist yet"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_prices (
            id          INTEGER PRIMARY KEY,
            title       VARCHAR,
            price_gbp   FLOAT,
            rating      VARCHAR,
            availability VARCHAR,
            scraped_at  TIMESTAMP,
            page        INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id          INTEGER,
            title       VARCHAR,
            price_gbp   FLOAT,
            scraped_at  TIMESTAMP,
            run_date    DATE
        )
    """)
    print("Database tables ready.")

def load_prices(df, conn):
    """Loads scraped data into DuckDB"""

    # Clear today's raw data and reload fresh
    conn.execute("DELETE FROM raw_prices")

    # Insert all rows from the DataFrame
    conn.execute("""
        INSERT INTO raw_prices
        SELECT
            ROW_NUMBER() OVER () as id,
            title,
            price_gbp,
            rating,
            availability,
            scraped_at::TIMESTAMP,
            page
        FROM df
    """)

    # Also append to price history (keeps all runs)
    conn.execute("""
        INSERT INTO price_history
        SELECT
            ROW_NUMBER() OVER () as id,
            title,
            price_gbp,
            scraped_at::TIMESTAMP,
            CURRENT_DATE as run_date
        FROM df
    """)

    count = conn.execute("SELECT COUNT(*) FROM raw_prices").fetchone()[0]
    print(f"Loaded {count} records into raw_prices.")

def run_quick_analysis(conn):
    """Shows some instant insights from the data"""
    print("\n--- Quick Analysis ---")

    print("\nTop 5 most expensive books:")
    result = conn.execute("""
        SELECT title, price_gbp, rating
        FROM raw_prices
        ORDER BY price_gbp DESC
        LIMIT 5
    """).fetchdf()
    print(result.to_string(index=False))

    print("\nAverage price by rating:")
    result = conn.execute("""
        SELECT
            rating,
            ROUND(AVG(price_gbp), 2) as avg_price,
            COUNT(*) as book_count
        FROM raw_prices
        GROUP BY rating
        ORDER BY avg_price DESC
    """).fetchdf()
    print(result.to_string(index=False))

    print("\nBooks under £15 (bargains):")
    result = conn.execute("""
        SELECT title, price_gbp
        FROM raw_prices
        WHERE price_gbp < 15
        ORDER BY price_gbp ASC
    """).fetchdf()
    print(result.to_string(index=False))
def detect_anomalies(conn):
    """
    Compares today's prices to yesterday's.
    Flags any book where price changed by more than 5%.
    This is the core of the 'alert engine'.
    """
    print("\n--- Price Anomaly Detection ---")

    anomalies = conn.execute("""
        WITH today AS (
            SELECT title, price_gbp, run_date
            FROM price_history
            WHERE run_date = CURRENT_DATE
        ),
        yesterday AS (
            SELECT title, price_gbp, run_date
            FROM price_history
            WHERE run_date = CURRENT_DATE - INTERVAL '1 day'
        )
        SELECT
            t.title,
            y.price_gbp                                    AS old_price,
            t.price_gbp                                    AS new_price,
            ROUND(t.price_gbp - y.price_gbp, 2)           AS change_gbp,
            ROUND(
                ((t.price_gbp - y.price_gbp) / y.price_gbp) * 100
            , 1)                                           AS change_pct
        FROM today t
        JOIN yesterday y ON t.title = y.title
        WHERE ABS(
                (t.price_gbp - y.price_gbp) / y.price_gbp
              ) > 0.05
        ORDER BY ABS(change_pct) DESC
    """).fetchdf()

    if anomalies.empty:
        print("No significant price changes detected today.")
        print("(Run the scraper again tomorrow to see real changes)")
    else:
        print(f"Found {len(anomalies)} price anomalies!")
        print(anomalies.to_string(index=False))

    return anomalies
if __name__ == "__main__":
    print("Connecting to database...")
    conn = duckdb.connect(DB_PATH)

    setup_database(conn)

    print("\nScraping latest prices...")
    df = scrape_books(max_pages=5)

    print("\nLoading into database...")
    load_prices(df, conn)

    run_quick_analysis(conn)
    detect_anomalies(conn)

    conn.close()
    print("\nDone! Data saved to database/retail.db")