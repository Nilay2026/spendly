import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "spendly.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def find_user_by_email(email):
    """Find a user by email. Used during registration to check duplicates."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(name, email, password):
    """Create a new user with hashed password. Used during registration."""
    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    conn.commit()
    conn.close()


def verify_user_login(email, password):
    """
    Verify user credentials for login.
    
    Args:
        email (str): User's email address
        password (str): Plain text password to verify
    
    Returns:
        dict-like object (sqlite3.Row) with user data if credentials valid
        None if email not found or password incorrect
    """
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    
    if user is None:
        # Email not found
        return None
    
    # Verify password against stored hash
    if check_password_hash(user['password_hash'], password):
        return user
    else:
        # Password incorrect
        return None


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def get_expenses_by_user_and_date_range(user_id, from_date, to_date):
    conn = get_db()
    rows = conn.execute(
        """SELECT * FROM expenses
           WHERE user_id = ? AND date >= ? AND date <= ?
           ORDER BY date DESC""",
        (user_id, from_date, to_date),
    ).fetchall()
    conn.close()
    return rows


def seed_db():
    """
    Seed the database with demo user and sample expenses.
    Idempotent — safe to call multiple times.
    """
    conn = get_db()

    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()

    if existing:
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("password123")),
    )
    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()["id"]

    sample_expenses = [
        (user_id, 12.50,  "Food",          "2026-04-01", "Lunch at cafe"),
        (user_id, 35.00,  "Transport",     "2026-04-02", "Monthly bus pass top-up"),
        (user_id, 120.00, "Bills",         "2026-04-03", "Electricity bill"),
        (user_id, 55.00,  "Health",        "2026-04-04", "Pharmacy"),
        (user_id, 18.99,  "Entertainment", "2026-04-05", "Streaming subscription"),
        (user_id, 64.75,  "Shopping",      "2026-04-06", "Clothing"),
        (user_id, 9.00,   "Other",         "2026-04-07", "Stationery"),
        (user_id, 22.30,  "Food",          "2026-04-08", "Groceries"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )

    conn.commit()
    conn.close()
