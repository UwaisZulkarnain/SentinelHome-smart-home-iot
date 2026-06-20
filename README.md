# 🏠 SentinelHome — Smart Home IoT Monitoring System
**ML for IoT | Group Project 2 | UTM 2025/2026**

---

## 👥 Team

| Name | Role |
|---|---|
| Uwais | Hardware + Firmware |
| Born + Harris | Favoriot Dashboard |
| Khamsah | ML Model (Anomaly Detection) |
| Aqasha | Demo + Testing |

---

## 🔧 Hardware

- **Board:** Seeed Studio XIAO ESP32S3
- **Sensors:** DHT11 (temp/humidity), PIR HC-SR501 (motion), MQ-2 (gas/smoke)
- **Actuators:** LED indicator, Buzzer

**Pin Mapping:**

| Sensor | XIAO Pin | GPIO |
|---|---|---|
| DHT11 | D10 | GPIO9 |
| PIR | D9 | GPIO8 |
| MQ-2 DO | D8 | GPIO7 |
| LED | D6 | GPIO43 |
| Buzzer | D7 | GPIO44 |

---

## 🚀 Quick Start

### Flash XIAO Firmware
1. Open project in VSCode with PlatformIO
2. Connect XIAO via USB
3. `pio run --target upload --upload-port COM10`
4. Turn on hotspot: **Uwais iph** / **sarrah123**
5. XIAO connects automatically and starts pushing data

### Run Local Dashboard
pip install flask requests
python dashboard.py
Open http://localhost:5000

### Collect ML Dataset (Khamsah)
pip install requests
python tools/collect_dataset.py

---

## ☁️ Supabase (Live Data)

- **Project URL:** https://ubcyktzfiylqirzpdqnu.supabase.co
- **Table:** sensor_readings
- **Anon Key:** (check WhatsApp group)
- **Data rate:** 1 row per 10 seconds

**Columns:** created_at, temperature, humidity, motion, gas, alarm

---

## 📡 XIAO HTTP API

When XIAO is on hotspot (172.20.10.2):
- Live data: http://172.20.10.2/data
- Format: {"t":25.0,"h":45.0,"m":0,"g":0,"a":0}

---

## 📁 Project Structure

MLT_IOT_Project_2/
├── src/
│   ├── main.cpp          # XIAO firmware
│   └── config.h          # Pin definitions
├── dashboard.py          # Flask web dashboard
├── monitor.py            # Terminal monitor
├── tools/
│   └── collect_dataset.py # Dataset collector for Khamsah
├── dataset/              # CSV datasets (gitignored)
└── platformio.ini

---

## 🧠 ML Pipeline (Khamsah)

- **Algorithm:** Isolation Forest
- **Features:** temperature, humidity, motion, gas, alarm
- **Training data:** normal baseline readings
- **Anomaly data:** triggered sensor events
- **Goal:** detect unusual sensor patterns = safety alert

---

## 📋 Demo Checklist (Aqasha)

- [ ] XIAO powered on, hotspot active
- [ ] dashboard.py running, open on browser
- [ ] Supabase table showing live rows
- [ ] Trigger PIR — motion detected
- [ ] Trigger MQ-2 — gas detected
- [ ] Blow on DHT11 — humidity spike
- [ ] Show ML anomaly detection result
- [ ] Favoriot dashboard live (Born)

---

## ⚠️ Notes

- XIAO cannot connect to UTM WiFi (captive portal)
- Always use Uwais phone hotspot for demo
- MQ-2 needs 20s warmup after power on
- PIR sensitivity adjusted — wave directly at dome to trigger