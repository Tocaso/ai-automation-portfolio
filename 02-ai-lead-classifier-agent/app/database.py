import sqlite3
from pathlib import Path

from app.schemas import LeadDecision, LeadIn

DB_PATH = Path("leads.db")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                source TEXT NOT NULL,
                route TEXT NOT NULL,
                score INTEGER NOT NULL,
                reason TEXT NOT NULL,
                action TEXT NOT NULL
            )
            """
        )


def save_lead(lead: LeadIn, decision: LeadDecision) -> int:
    init_db()
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO leads
                (name, email, message, source, route, score, reason, action)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lead.name,
                lead.email,
                lead.message,
                lead.source,
                decision.classification.route.value,
                decision.classification.score,
                decision.classification.reason,
                decision.action,
            ),
        )
    return int(cursor.lastrowid)