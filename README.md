# SentinelHome — Smart Home IoT Monitoring System
ML for IoT | Group Project 2 | UTM 2025/2026

---

## Team

| Name | Role |
|---|---|
| Uwais | Hardware, Firmware, Data Collection |
| Born + Harris | Favoriot / Node-RED Dashboard |
| Khamsah | ML Model |
| Aqasha | Demo + Presentation |

---

## What Uwais Already Did

- XIAO ESP32S3 wired and working (DHT11, PIR, MQ-2, LED, Buzzer)
- Firmware running with multi-class classification, night mode, motion timer, NTP sync
- Live data pushing to Supabase every 2 seconds when hotspot is on
- Python dashboard at localhost:5000
- All datasets generated and in dataset/ folder
- GitHub repo set up with all files

Everyone else just needs to do their specific part below.

---

## Files

| File | What it does |
|---|---|
| src/main.cpp | XIAO firmware |
| src/config.h | Pin definitions |
| dashboard.py | Live Python dashboard, pulls from XIAO direct with Supabase fallback |
| monitor.py | Terminal serial monitor, needs USB connection to XIAO |
| simulator.py | Synthetic dataset generator |
| tools/collect_serial.py | Real data collector via USB serial |
| dataset/ | All CSV files |

---

## Hardware Pins

| Sensor | XIAO Pin | GPIO |
|---|---|---|
| DHT11 | D10 | GPIO9 |
| PIR | D9 | GPIO8 |
| MQ-2 DO | D8 | GPIO7 |
| LED | D6 | GPIO43 |
| Buzzer | D7 | GPIO44 |

XIAO hotspot: Uwais iph / sarrah123
Static IP: 172.20.10.2
Live data: http://172.20.10.2/data

---

## Supabase

URL: https://ubcyktzfiylqirzpdqnu.supabase.co
Table: sensor_readings
Anon key: check WhatsApp

Columns:
```
created_at, temperature, humidity, motion, gas, alarm,
is_night, motion_duration_sec, alert_class, reason
```

---

## Favoriot

Device Developer ID: SentinelHome_XIAO@emerizzanie
API Key: check WhatsApp

---

## Dataset

All CSVs are in dataset/ folder.

Real data collected from actual XIAO:

| File | Description |
|---|---|
| sensor_raw_day_real.csv | Real day baseline, raw |
| sensor_processed_day_real.csv | Real day baseline, processed |
| sensor_raw_20260621_real_night_data.csv | Real night baseline, raw |
| sensor_processed_20260621_real_night_data.csv | Real night baseline, processed |

Synthetic data generated via simulator.py (3000 rows each):

| File | Class | Context |
|---|---|---|
| sensor_class0_day_raw/processed.csv | 0 Normal | Day |
| sensor_class0_night_raw/processed.csv | 0 Normal | Night |
| sensor_class1_day_raw/processed.csv | 1 Comfort Alert | Day |
| sensor_class1_night_raw/processed.csv | 1 Comfort Alert | Night |
| sensor_class2_day_raw/processed.csv | 2 Warning | Day |
| sensor_class2_night_raw/processed.csv | 2 Warning | Night |
| sensor_class3_day_raw/processed.csv | 3 Danger | Day |
| sensor_class3_night_raw/processed.csv | 3 Danger | Night |

Raw file columns:
```
created_at, temperature, humidity, motion, gas, is_night, motion_duration_sec
```

Processed file columns:
```
created_at, temperature, humidity, motion, gas, alarm, is_night, motion_duration_sec, alert_class, reason
```

Class definitions:

| Class | Label | Trigger |
|---|---|---|
| 0 | Normal | Baseline temp/humidity, no gas, normal motion for time of day |
| 1 | Comfort Alert | Temp 30-35C or humidity 70-80% or brief night motion under 5s |
| 2 | Warning | Temp 35-40C or humidity 80%+ or sustained night motion 5-15s |
| 3 | Danger | Gas detected or temp 40C+ or night intrusion 15s+ |

---

## Khamsah

1. Clone repo or download dataset/ folder
2. Use processed CSVs for training — they have the alert_class column
3. Train on these features:

```
temperature, humidity, motion, gas, is_night, motion_duration_sec
```

Target column: alert_class (0, 1, 2, 3)

4. Send Uwais the trained model as sentinelhome_model.pkl when done

Quick start:

```python
import pandas as pd
import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

files = glob.glob("dataset/*_processed.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

features = ["temperature","humidity","motion","gas","is_night","motion_duration_sec"]
X = df[features]
y = df["alert_class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

with open("sentinelhome_model.pkl", "wb") as f:
    pickle.dump(model, f)
```

---

## Born + Harris

Two options — pick whichever, or do both.

### Option A — Favoriot
Limited to 500 API calls/day on free tier. Only suitable for short demo windows, not continuous logging. Device Developer ID and API key in WhatsApp.

### Option B — Node-RED (recommended, no limits)
Pulls from the same Supabase table the Python dashboard uses.

Steps:
1. Install the `node-red-dashboard` palette (Menu → Manage palette → Install)
2. Add an `inject` node, set to repeat every 10-30 seconds
3. Add an `http request` node (GET method), URL:
   ```
   https://ubcyktzfiylqirzpdqnu.supabase.co/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=1
   ```
   Headers:
   ```
   apikey: check WhatsApp
   Authorization: Bearer check WhatsApp
   ```
4. Add a `json` node to parse the response
5. Wire parsed fields into dashboard widgets:
   temperature, humidity, motion, gas, alarm, is_night, motion_duration_sec, alert_class, reason

Flow: inject → http request → json → dashboard widgets

---

## Demo Checklist

- XIAO cannot connect to UTM WiFi, always use Uwais hotspot
- MQ-2 needs 20 seconds warmup after power on
- PIR sensitivity adjusted, wave directly at dome to trigger
- Night mode auto-detects 10pm-7am as night, 7am-10pm as day
- Night mode can be manually overridden via dashboard buttons
- alert_class column in Supabase and CSVs — do not rename to class (reserved word in PostgreSQL)