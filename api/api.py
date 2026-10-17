import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

BASE = Path(__file__).resolve().parent.parent      # k2-meter-demo folder
DB_PATH = BASE / "data" / "mdms.db"
DASHBOARD = BASE / "dashboard" / "index.html"
ONLINE_SECONDS = 30       # itne second mein reading aayi to meter "online"

app = FastAPI(title="K2 Meter Demo API")


def query(sql, params=()):
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in db.execute(sql, params).fetchall()]
    finally:
        db.close()


@app.get("/")
def dashboard():
    return FileResponse(DASHBOARD)


@app.get("/api/summary")
def summary():
    ok = query("SELECT COUNT(*) AS n FROM readings")[0]["n"]
    bad = query("SELECT COUNT(*) AS n FROM rejected")[0]["n"]
    meters = query("SELECT COUNT(DISTINCT meter_id) AS n FROM readings")[0]["n"]
    reasons = query(
        "SELECT substr(reason, 1, instr(reason || ':', ':') - 1) AS reason, "
        "COUNT(*) AS count FROM rejected GROUP BY 1 ORDER BY count DESC"
    )
    return {"good": ok, "rejected": bad, "meters": meters, "reasons": reasons}


@app.get("/api/meters")
def meters():
    rows = query(
        """SELECT r.meter_id, r.ts, r.kwh, r.voltage, r.current, r.received_at
           FROM readings r
           JOIN (SELECT meter_id, MAX(id) AS mid FROM readings GROUP BY meter_id) m
             ON r.id = m.mid
           ORDER BY r.meter_id"""
    )
    now = datetime.utcnow()
    for r in rows:
        age = (now - datetime.fromisoformat(r["received_at"])).total_seconds()
        r["status"] = "online" if age <= ONLINE_SECONDS else "offline"
        r["age_seconds"] = int(age)
    return rows


@app.get("/api/meters/{meter_id}/readings")
def meter_readings(meter_id: str, limit: int = 60):
    limit = max(1, min(limit, 1000))
    rows = query(
        "SELECT ts, seq, kwh, voltage, current FROM readings "
        "WHERE meter_id = ? ORDER BY id DESC LIMIT ?",
        (meter_id, limit),
    )
    if not rows:
        raise HTTPException(404, f"No readings for {meter_id}")
    return list(reversed(rows))


@app.get("/api/rejected")
def rejected(limit: int = 20):
    limit = max(1, min(limit, 200))
    return query(
        "SELECT reason, raw, received_at FROM rejected ORDER BY id DESC LIMIT ?",
        (limit,),
    )