import json, sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

# ====== settings ======
BROKER = "localhost"
PORT = 1883
TOPIC = "meters/+/readings"
DB_PATH = "data/mdms.db"
V_MIN, V_MAX = 180.0, 280.0     # voltage ka valid range
I_MAX = 100.0                   # current ka max (A)
# ======================

db = sqlite3.connect(DB_PATH, check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS readings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_id TEXT, ts TEXT, seq INTEGER,
    kwh REAL, voltage REAL, current REAL,
    received_at TEXT)""")
db.execute("""CREATE TABLE IF NOT EXISTS rejected(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reason TEXT, raw TEXT, received_at TEXT)""")
db.commit()

last = {}   # har meter ki last seq aur kwh
stats = {"ok": 0, "rejected": 0}

def validate(p):
    """Sahi ho to None, galat ho to reason (text) return karta hai"""
    for k in ("meter_id", "ts", "seq", "kwh", "voltage", "current"):
        if k not in p:
            return f"missing_field:{k}"
    try:
        datetime.strptime(p["ts"], "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return "bad_timestamp"
    if not (V_MIN <= p["voltage"] <= V_MAX):
        return f"voltage_out_of_range:{p['voltage']}"
    if not (0 <= p["current"] <= I_MAX):
        return f"current_out_of_range:{p['current']}"
    if p["kwh"] < 0:
        return "negative_kwh"
    prev = last.get(p["meter_id"])
    if prev:
        if p["seq"] <= prev["seq"]:
            return f"duplicate_or_old_seq:{p['seq']}"
        if p["kwh"] < prev["kwh"]:
            return "kwh_decreased"
    return None

def on_message(client, userdata, msg):
    now = datetime.utcnow().isoformat()
    raw = msg.payload.decode(errors="replace")
    try:
        p = json.loads(raw)
    except Exception:
        reason = "invalid_json"
    else:
        reason = validate(p)

    if reason:
        db.execute("INSERT INTO rejected(reason,raw,received_at) VALUES(?,?,?)",
                   (reason, raw, now))
        stats["rejected"] += 1
        print(f"REJECT  {reason}  <- {raw[:80]}")
    else:
        db.execute("""INSERT INTO readings(meter_id,ts,seq,kwh,voltage,current,received_at)
                      VALUES(?,?,?,?,?,?,?)""",
                   (p["meter_id"], p["ts"], p["seq"], p["kwh"],
                    p["voltage"], p["current"], now))
        last[p["meter_id"]] = {"seq": p["seq"], "kwh": p["kwh"]}
        stats["ok"] += 1
        print(f"OK      {p['meter_id']} seq={p['seq']} kwh={p['kwh']} V={p['voltage']}")
    db.commit()
    print(f"        total ok={stats['ok']} rejected={stats['rejected']}")

def on_connect(client, userdata, flags, reason_code, properties):
    print("HES connected to broker, listening on", TOPIC)
    client.subscribe(TOPIC)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="k2-hes")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_forever()