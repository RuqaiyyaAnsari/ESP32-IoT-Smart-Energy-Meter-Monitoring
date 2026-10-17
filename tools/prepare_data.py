import pandas as pd

# 1. Dataset ki shuru ki rows padho
df = pd.read_csv(
    "data/household_power_consumption.txt",
    sep=";", na_values=["?"], nrows=2000, low_memory=False,
)

# 2. Missing wali rows hatao, pehli 300 rakho
df = df.dropna().head(300).reset_index(drop=True)

# 3. kW ko 1 minute ki kWh mein badlo, phir cumulative banao
df["kwh_step"] = df["Global_active_power"].astype(float) / 60.0
df["kwh_total"] = df["kwh_step"].cumsum()

volts = df["Voltage"].astype(float).round(1).tolist()
amps = df["Global_intensity"].astype(float).round(2).tolist()
kwh = df["kwh_total"].round(4).tolist()

def arr(name, values):
    return f"const float {name}[] = {{" + ", ".join(str(v) for v in values) + "};\n"

# 4. ESP32 ke liye header file likho
with open("esp32_meter/readings.h", "w") as f:
    f.write(f"const int N_READINGS = {len(df)};\n")
    f.write(arr("VOLT", volts))
    f.write(arr("CURR", amps))
    f.write(arr("KWH", kwh))

# 5. Aage simulator ke liye CSV bhi bana lo
df[["Date", "Time", "Voltage", "Global_intensity", "kwh_total"]].to_csv(
    "data/sample.csv", index=False
)
print("Done:", len(df), "rows")