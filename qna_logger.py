# qna_logger.py
import csv, os, hashlib, datetime, pytz
from typing import Optional, Dict, Any

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "qna_log.csv")

DEFAULT_HEADERS = [
    "ts_myt",          # 2025-08-29 09:41:12 +08
    "from_hash",       # sha1 of wa_from (privacy)
    "lang",            # BM / EN
    "intent",          # buy / test_drive / hours / warranty / about / default / error
    "after_hours",     # 0/1
    "frozen",          # 0/1
    "asked",           # user question
    "answered",        # 0/1 (was a non-empty answer returned)
    "answer_len",      # len(answer)
    "has_link",        # 0/1
    "status",          # ok / empty / error
    "answer",          # raw answer text
]

def _ensure_file():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(DEFAULT_HEADERS)

def _sha1(s: str) -> str:
    return hashlib.sha1((s or "").encode("utf-8")).hexdigest()[:12]

def _now_myt_str():
    tz = pytz.timezone("Asia/Kuala_Lumpur")
    return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %z")

def _has_link(text: str) -> int:
    t = (text or "").lower()
    for marker in ("http://", "https://"):
        if marker in t:
            return 1
    return 0

def log_qna(
    wa_from: str,
    asked: str,
    answer: str,
    *,
    lang: str = "",
    intent: str = "",
    after_hours: bool = False,
    frozen: bool = False,
    status: str = "ok",
):
    """
    Append one row to logs/qna_log.csv with normalized fields.
    """
    _ensure_file()
    row = [
        _now_myt_str(),
        _sha1(wa_from),
        (lang or "").upper(),
        (intent or "").lower(),
        1 if after_hours else 0,
        1 if frozen else 0,
        asked or "",
        1 if (answer or "").strip() else 0,
        len(answer or ""),
        _has_link(answer or ""),
        status,
        answer or "",
    ]
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)
