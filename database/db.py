import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "database/spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    # Insert demo user — skip silently if email already exists
    conn.execute(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("password123")),
    )
    conn.commit()

    user = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()
    user_id = user["id"]

    # Only seed expenses if none exist for this user
    count = conn.execute(
        "SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    if count == 0:
        sample_expenses = [
            (user_id, 450.00,  "Food",          "2026-04-01", "Groceries at DMart"),
            (user_id, 120.00,  "Transport",     "2026-04-02", "Ola ride to office"),
            (user_id, 1200.00, "Bills",         "2026-04-03", "Electricity bill"),
            (user_id, 800.00,  "Health",        "2026-04-05", "Pharmacy — vitamins"),
            (user_id, 350.00,  "Entertainment", "2026-04-07", "Movie tickets"),
            (user_id, 2500.00, "Shopping",      "2026-04-09", "New headphones"),
            (user_id, 60.00,   "Other",         "2026-04-10", "Parking fee"),
            (user_id, 300.00,  "Food",          "2026-04-12", "Dinner with friends"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses,
        )
        conn.commit()

    conn.close()
