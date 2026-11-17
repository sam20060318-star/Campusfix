"""SQLite storage for CampusFix.

One database file is shared by the student and staff sides of the app.
Running init_db() again never deletes existing reports.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from werkzeug.security import generate_password_hash

STATUSES = ("Submitted", "In Progress", "Resolved")
REPORT_FIELDS = ("title", "location", "category", "description")

# Demonstration accounts only (fictional). Never put real passwords here.
DEMO_USERS = (
    ("staff", "staff123", "staff"),
    ("student", "student123", "student"),
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    location        TEXT NOT NULL,
    category        TEXT NOT NULL,
    description     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'Submitted'
                    CHECK (status IN ('Submitted', 'In Progress', 'Resolved')),
    resolution_note TEXT NOT NULL DEFAULT '',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS users (
    username      TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('student', 'staff'))
);
"""


def _casefold(value):
    return value.casefold() if isinstance(value, str) else value


@contextmanager
def connect(db_path):
    """Open a connection, commit on success, roll back on error, always close."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Case-insensitive comparison that also works beyond ASCII letters.
    conn.create_function("CASEFOLD", 1, _casefold, deterministic=True)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path):
    """Create tables and demo accounts if they are missing. Safe to re-run."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        for username, password, role in DEMO_USERS:
            exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role),
                )


def _report(row):
    return dict(row) if row else None


# Jira CF-4｜S1 提交問題回報
def create_report(db_path, values):
    with connect(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO reports (title, location, category, description) VALUES (?, ?, ?, ?)",
            tuple(values[field] for field in REPORT_FIELDS),
        )
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _report(row)


def list_reports(db_path, keyword="", location=""):
    """Newest first.

    keyword: case-insensitive, matches title OR description.
    location: case-insensitive exact match on the whole location.
    When both are given, a report must satisfy both (AND).
    """
    clauses, params = [], []
    keyword = keyword.strip().casefold()
    location = " ".join(location.split()).casefold()
    if keyword:
        clauses.append("(instr(CASEFOLD(title), ?) > 0 OR instr(CASEFOLD(description), ?) > 0)")
        params += [keyword, keyword]
    if location:
        clauses.append("CASEFOLD(location) = ?")
        params.append(location)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect(db_path) as conn:
        rows = conn.execute(f"SELECT * FROM reports {where} ORDER BY id DESC", params).fetchall()
    return [_report(row) for row in rows]


# Jira CF-6｜S3 查看報修詳情與狀態
def get_report(db_path, report_id):
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
    return _report(row)


# Jira CF-8｜S5 更新報修狀態
def update_status(db_path, report_id, status, resolution_note):
    """Save status and note together. Returns the updated report or None."""
    with connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE reports SET status = ?, resolution_note = ?, updated_at = datetime('now') WHERE id = ?",
            (status, resolution_note, report_id),
        )
        if cursor.rowcount == 0:
            return None
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
    return _report(row)


def list_locations(db_path):
    """Distinct stored locations, used as suggestions so filters match saved values."""
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT MIN(location) AS location FROM reports GROUP BY CASEFOLD(location) ORDER BY CASEFOLD(location)"
        ).fetchall()
    return [row["location"] for row in rows]


def get_user(db_path, username):
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


def seed_demo_reports(db_path):
    """Insert three fictional reports, only when the table is empty."""
    samples = (
        ("走廊燈故障", "B 棟", "設施", "演講廳外面的走廊燈不亮。"),
        ("Wi-Fi 一直斷線", "圖書館", "Wi-Fi 與資訊", "二樓自習區附近的 Wi-Fi 連線反覆中斷。"),
        ("投影機無法開機", "教室 A101", "教室設備", "按下電源鍵後投影機沒有反應。"),
    )
    with connect(db_path) as conn:
        if conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]:
            return 0
        conn.executemany(
            "INSERT INTO reports (title, location, category, description) VALUES (?, ?, ?, ?)", samples
        )
    return len(samples)
