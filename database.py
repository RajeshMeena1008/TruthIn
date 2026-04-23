"""
database.py
SQLite persistence for scan history.
"""

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "foodscan_history.db")


def init_db():
    """Create database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            health_score INTEGER NOT NULL,
            scan_type TEXT DEFAULT 'general',
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_scan(food_name: str, health_score: int, scan_type: str = "general"):
    """Insert a new scan record."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO scans (food_name, health_score, scan_type, timestamp) VALUES (?,?,?,?)",
        (food_name, int(health_score), scan_type, ts)
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 100) -> list:
    """Fetch recent scan history, newest first."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, food_name, health_score, scan_type, timestamp FROM scans ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def clear_history():
    """Delete all scan records."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM scans")
    conn.commit()
    conn.close()
