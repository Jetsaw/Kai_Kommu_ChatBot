import sqlite3, os
from config import DB_PATH

DDL = """
CREATE TABLE IF NOT EXISTS tickets(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wa_from TEXT,
  body TEXT,
  reason TEXT,
  after_hours INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'open',
  claimed_by TEXT
);
"""

def init_db():
    d = os.path.dirname(DB_PATH)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute(DDL)

def create_ticket(wa_from: str, body: str, reason: str, after_hours: bool) -> int:
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO tickets(wa_from, body, reason, after_hours) VALUES (?,?,?,?)",
                    (wa_from, body, reason, 1 if after_hours else 0))
        con.commit()
        return cur.lastrowid
