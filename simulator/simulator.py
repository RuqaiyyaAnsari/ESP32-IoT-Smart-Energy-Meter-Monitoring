import csv, json, time, random, sys
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# ====== settings ======
BROKER = "localhost"
PORT = 1883
N_METERS = 5            # kitne virtual meters
INTERVAL = 2            # har reading ke beech seconds
INJECT_BAD_DATA = True # True karne par kuch kharab readings jayengi
CSV_PATH = "data/sample.csv"
# ======================

# Dataset padho
rows = []
with open(CSV_PATH, newline="") as f:
    for r in csv.DictReader(f):
        rows.append(r)
print(f"Loaded {len(rows)} rows, {N_METERS} meters")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="k2-simulator")
client.connect(BROKER, PORT)
client.loop_start()

# Har meter ke liye thoda alag scale, taaki sab ek jaise na dikhein
meters = []
for i in range(N_METERS):
    meters.append({
        "id": f"K2-MTR-{i+1:04d}",
        "scale": round(random.uniform(0.7, 1.4), 2),
        "offset": random.randint(0, len(rows) - 1),
        "seq": 0,
    })

step = 0
try:
    while True:
        for m in meters:
            r = rows[(m["offset"] + step) % len(rows)]
            payload = {
                "meter_id": m["id"],
                "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "seq": m["seq"],
                "kwh": round(float(r["kwh_total"]) * m["scale"], 4),
                "voltage": float(r["Voltage"]),
                "current": round(float(r["Global_intensity"]) * m["scale"], 2),
            }

            # Bad data testing ke liye (HES validator pakadega)
            if INJECT_BAD_DATA:
                x = random.random()
                if x < 0.03:
                    payload["voltage"] = 0            # out-of-range
                elif x < 0.06:
                    del payload["kwh"]                # missing field
                elif x < 0.09 and m["seq"] > 0:
                    payload["seq"] = m["seq"] - 1     # duplicate/old seq

            topic = f"meters/{m['id']}/readings"
            client.publish(topic, json.dumps(payload))
            print(topic, payload)
            m["seq"] += 1
        step += 1
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("Stopped")
    client.loop_stop()
    client.disconnect()