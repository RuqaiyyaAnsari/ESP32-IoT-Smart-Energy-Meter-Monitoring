import sqlite3
db = sqlite3.connect("data/mdms.db")
print("Good readings :", db.execute("SELECT COUNT(*) FROM readings").fetchone()[0])
print("Rejected      :", db.execute("SELECT COUNT(*) FROM rejected").fetchone()[0])
print("\nRejection reasons:")
for r in db.execute("SELECT substr(reason,1,22), COUNT(*) FROM rejected GROUP BY 1"):
    print("  ", r)
print("\nLatest readings per meter:")
for r in db.execute("""SELECT meter_id, MAX(ts), kwh, voltage FROM readings GROUP BY meter_id"""):
    print("  ", r)