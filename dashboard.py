from flask import Flask, render_template_string, jsonify, request
import requests
from datetime import datetime
import serial
import threading
import time
import joblib
import numpy as np
import os
import re

app = Flask(__name__)

XIAO_IP = "172.20.10.2"
XIAO_URL = f"http://{XIAO_IP}/data"
SUPABASE_URL = "https://ubcyktzfiylqirzpdqnu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViY3lrdHpmaXlscWlyenBkcW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4MDkxNjQsImV4cCI6MjA5NzM4NTE2NH0.Gu0jBFdVnsBMFF2VWliTnoKtBqCt_-IwSQfnoe2ts9c"
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
SERIAL_PORT = "COM10"
SERIAL_BAUD = 115200

MODEL_PATH = "ML/ML\new_random_forest_model_n70.pkl"
SCALER_PATH = "ML\scaler_n70.pkl"

ml_model = None
ml_scaler = None

try:
    ml_model = joblib.load(MODEL_PATH)
    ml_scaler = joblib.load(SCALER_PATH)
    print("ML model loaded successfully")
except Exception as e:
    print(f"ML model not loaded: {e}")

def ml_predict(temperature, humidity, motion, gas, is_night, motion_duration_sec):
    if ml_model is None or ml_scaler is None:
        return None, None
    try:
        import pandas as pd
        numeric = pd.DataFrame([[temperature, humidity, gas, motion_duration_sec]],
                               columns=["temperature", "humidity", "gas", "motion_duration_sec"])
        numeric_scaled = ml_scaler.transform(numeric)
        features = [[numeric_scaled[0][0], numeric_scaled[0][1], motion,
                     numeric_scaled[0][2], is_night, numeric_scaled[0][3]]]
        prediction = int(ml_model.predict(features)[0])
        confidence = float(ml_model.predict_proba(features)[0][prediction])
        return prediction, round(confidence, 3)
    except Exception as e:
        print(f"ML prediction error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

current_mode = "local"
serial_data = None
serial_error = None
serial_thread = None
serial_running = False

def serial_reader():
    global serial_data, serial_error, serial_running
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=2)
        serial_error = None
        time.sleep(2)
        while serial_running:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if line.startswith("T:"):
                    tokens = line.split()
                    d = {}
                    for tok in tokens:
                        if ":" in tok:
                            k, v = tok.split(":", 1)
                            d[k] = v
                    serial_data = {
                        "temperature": float(d.get("T", 0)),
                        "humidity": float(d.get("H", 0)),
                        "motion": int(d.get("M", 0)),
                        "gas": int(d.get("G", 0)),
                        "alarm": int(d.get("A", 0)),
                        "is_night": int(d.get("N", 0)),
                        "motion_duration_sec": int(d.get("DUR", 0)),
                        "alert_class": int(d.get("CLASS", 0)),
                        "reason": d.get("REASON", "normal"),
                        "xiao_push": 0,
                        "source": "serial",
                        "ok": True,
                        "created_at": datetime.utcnow().isoformat()
                    }
                    ml_val = re.search(r'ML:(\d+)', line)
                    conf_val = re.search(r'CONF:([\d.]+)', line)
                    serial_data["ml_class"] = int(ml_val.group(1)) if ml_val else None
                    serial_data["ml_confidence"] = float(conf_val.group(1)) if conf_val else None
            except Exception:
                pass
        ser.close()
    except Exception as e:
        serial_error = str(e)
        serial_data = None

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/latest")
def latest():
    global current_mode
    if current_mode == "serial":
        if serial_error:
            return jsonify({
                "ok": False,
                "source": "serial",
                "error": "Serial port unavailable",
                "message": f"Could not open {SERIAL_PORT}: {serial_error}",
                "action": "Make sure XIAO is connected via USB and no other program is using COM10 (close monitor.py or collect_serial.py)."
            })
        if serial_data is None:
            return jsonify({
                "ok": False,
                "source": "serial",
                "error": "No serial data yet",
                "message": "Serial port opened but no data received yet.",
                "action": "Wait a few seconds for XIAO to send data, or check that XIAO is powered on."
            })
        result = dict(serial_data)
        pred, conf = ml_predict(
            result.get("temperature",0), result.get("humidity",0),
            result.get("motion",0), result.get("gas",0),
            result.get("is_night",0), result.get("motion_duration_sec",0)
        )
        print(f"ML debug - pred:{pred} conf:{conf} features: T:{result.get('temperature')} H:{result.get('humidity')} M:{result.get('motion')} G:{result.get('gas')} N:{result.get('is_night')} DUR:{result.get('motion_duration_sec')}")
        if result.get("ml_class") is None or result.get("ml_confidence") is None:
            result["ml_class"] = pred
            result["ml_confidence"] = conf
            result["ml_source"] = "flask"
        else:
            result["ml_source"] = "xiao"
        return jsonify(result)

    elif current_mode == "local":
        try:
            r = requests.get(XIAO_URL, timeout=2)
            d = r.json()
            data = {
                "ok": True,
                "source": "local",
                "temperature": d.get("t", 0),
                "humidity": d.get("h", 0),
                "motion": d.get("m", 0),
                "gas": d.get("g", 0),
                "alarm": d.get("a", 0),
                "is_night": d.get("n", 0),
                "motion_duration_sec": d.get("dur", 0),
                "alert_class": d.get("class", 0),
                "reason": d.get("reason", "normal"),
                "xiao_push": d.get("push", 0),
                "created_at": datetime.utcnow().isoformat()
            }
            data["ml_class"] = d.get("ml_class")
            data["ml_confidence"] = d.get("ml_conf")
            if data.get("ml_class") is None or data.get("ml_confidence") is None:
                pred, conf = ml_predict(
                    d.get("t",0), d.get("h",0), d.get("m",0),
                    d.get("g",0), d.get("n",0), d.get("dur",0)
                )
                data["ml_class"] = pred
                data["ml_confidence"] = conf
                data["ml_source"] = "flask"
            else:
                data["ml_source"] = "xiao"
            return jsonify(data)
        except Exception:
            return jsonify({
                "ok": False,
                "source": "local",
                "error": "XIAO unreachable on local network",
                "message": f"Could not reach XIAO at {XIAO_IP}.",
                "action": "Make sure your laptop and XIAO are on the same hotspot (Uwais iph). XIAO must be powered on."
            })

    else:  # supabase
        try:
            r = requests.get(
                f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=1",
                headers=HEADERS, timeout=10
            )
            print(f"Supabase status: {r.status_code}, body: {r.text[:200]}")
            data = r.json()
            if not data:
                return jsonify({
                    "ok": False,
                    "source": "supabase",
                    "error": "No data in Supabase",
                    "message": "Supabase is reachable but has no rows.",
                    "action": "Switch to Local Network mode and turn ON the XIAO Supabase push first."
                })
            row = data[0]
            age_sec = (datetime.utcnow() - datetime.fromisoformat(row["created_at"].replace("Z","").split("+")[0])).total_seconds()
            row["ok"] = True
            row["source"] = "supabase"
            row["data_age_sec"] = int(age_sec)
            if age_sec > 30:
                row["stale_warning"] = f"Data is {int(age_sec)}s old. XIAO may not be pushing."
            if row.get("ml_class") is not None and row.get("ml_confidence") is not None:
                row["ml_source"] = "xiao"
            else:
                pred, conf = ml_predict(
                    row.get("temperature",0), row.get("humidity",0),
                    row.get("motion",0), row.get("gas",0),
                    row.get("is_night",0), row.get("motion_duration_sec",0)
                )
                row["ml_class"] = pred
                row["ml_confidence"] = conf
                row["ml_source"] = "flask"
            return jsonify(row)
        except Exception as e:
            print(f"Supabase error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "ok": False,
                "source": "supabase",
                "error": "Supabase unreachable",
                "message": "Could not reach Supabase.",
                "action": "Check your internet connection."
            })

@app.route("/api/mode", methods=["POST"])
def set_mode():
    global current_mode, serial_thread, serial_running
    mode = request.json.get("mode")
    if mode not in ("serial", "local", "supabase"):
        return jsonify({"ok": False, "error": "Invalid mode"})

    if mode == "serial" and current_mode != "serial":
        serial_running = True
        serial_thread = threading.Thread(target=serial_reader, daemon=True)
        serial_thread.start()
    elif mode != "serial" and current_mode == "serial":
        serial_running = False

    current_mode = mode
    return jsonify({"ok": True, "mode": current_mode})

@app.route("/api/night", methods=["POST"])
def set_night():
    action = request.json.get("action")
    url_map = {
        "day": f"http://{XIAO_IP}/night?on=0",
        "night": f"http://{XIAO_IP}/night?on=1",
        "auto": f"http://{XIAO_IP}/night?auto=1"
    }
    url = url_map.get(action)
    if not url:
        return jsonify({"ok": False, "error": "Invalid action"})
    try:
        r = requests.get(url, timeout=2)
        return jsonify({"ok": True, "result": r.json()})
    except Exception:
        return jsonify({
            "ok": False,
            "error": "XIAO unreachable",
            "message": "Could not reach XIAO to change night mode.",
            "action": "Night mode toggle requires Local Network mode. Switch to Local Network first."
        })

@app.route("/api/supabase_push", methods=["POST"])
def set_supabase_push():
    enabled = request.json.get("enabled")
    url = f"http://{XIAO_IP}/supabase?on={'1' if enabled else '0'}"
    try:
        r = requests.get(url, timeout=2)
        return jsonify({"ok": True, "result": r.json()})
    except Exception:
        return jsonify({
            "ok": False,
            "error": "XIAO unreachable",
            "message": "Could not reach XIAO to toggle Supabase push.",
            "action": "Supabase push toggle requires Local Network mode. Switch to Local Network first."
        })

@app.route("/api/history")
def history():
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=50",
            headers=HEADERS, timeout=5
        )
        return jsonify(r.json())
    except Exception:
        return jsonify([])

@app.route("/api/alerts")
def alerts():
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=100",
            headers=HEADERS, timeout=5
        )
        rows = r.json()
        return jsonify([row for row in rows if row.get("motion") or row.get("gas") or row.get("alarm")][:20])
    except Exception:
        return jsonify([])

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SentinelHome Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Segoe UI',sans-serif; background:#0a0e1a; color:#e2e8f0; min-height:100vh; font-size:15px; }
  .header { background:linear-gradient(135deg,#1e3a5f,#0f2027); padding:20px 30px;
    display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #1e3a5f; }
  .header h1 { font-size:1.6rem; color:#38bdf8; letter-spacing:2px; }
  .header .subtitle { font-size:0.8rem; color:#64748b; margin-top:4px; }
  .container { max-width:1280px; aspect-ratio:16/9; margin:0 auto; padding:24px; }
  .controls { background:#1e293b; border-radius:12px; padding:18px; margin-bottom:20px; border:1px solid #334155; }
  .control-row { display:flex; align-items:center; gap:12px; margin-bottom:14px; flex-wrap:wrap; }
  .control-row:last-child { margin-bottom:0; }
  .control-label { font-size:0.8rem; color:#94a3b8; min-width:140px; font-weight:600; }
  .btn { background:#334155; color:#e2e8f0; border:none; padding:8px 16px; border-radius:8px;
    cursor:pointer; font-size:0.8rem; font-weight:600; transition:all 0.15s; }
  .btn:hover { background:#475569; }
  .btn.active-serial { background:#f59e0b; color:#0a0e1a; }
  .btn.active-local { background:#38bdf8; color:#0a0e1a; }
  .btn.active-supabase { background:#a855f7; color:#fff; }
  .btn.active-night { background:#6366f1; color:#fff; }
  .btn.active-day { background:#fbbf24; color:#0a0e1a; }
  .btn.active-auto { background:#22c55e; color:#0a0e1a; }
  .btn.active-on { background:#22c55e; color:#0a0e1a; }
  .btn.active-off { background:#ef4444; color:#fff; }
  .source-tag { font-size:0.7rem; padding:2px 10px; border-radius:10px; font-weight:700; }
  .tag-serial { background:rgba(245,158,11,0.2); color:#f59e0b; }
  .tag-local { background:rgba(56,189,248,0.2); color:#38bdf8; }
  .tag-supabase { background:rgba(168,85,247,0.2); color:#a855f7; }
  .error-banner { background:#7f1d1d; border:1px solid #ef4444; color:#fecaca;
    padding:14px 18px; border-radius:10px; margin-bottom:20px; display:none; }
  .error-banner.show { display:block; }
  .warn-banner { background:#78350f; border:1px solid #f59e0b; color:#fde68a;
    padding:10px 18px; border-radius:10px; margin-bottom:20px; display:none; }
  .warn-banner.show { display:block; }
  .err-title { font-weight:700; margin-bottom:4px; }
  .err-action { font-size:0.85rem; margin-top:6px; opacity:0.85; }
  .cards { display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin-bottom:24px; }
  .card { background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; text-align:center; }
  .card-icon { font-size:2rem; margin-bottom:8px; }
  .card-value { font-size:2rem; font-weight:700; margin:6px 0; }
  .card-label { font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; }
  .card-status { font-size:0.75rem; font-weight:600; padding:3px 10px; border-radius:10px; display:inline-block; margin-top:6px; }
  .ok { background:rgba(34,197,94,0.15); color:#22c55e; }
  .warn { background:rgba(245,158,11,0.15); color:#f59e0b; }
  .danger { background:rgba(239,68,68,0.15); color:#ef4444; }
  .charts { display:grid; grid-template-columns:2fr 1fr; gap:16px; margin-bottom:24px; }
  .panel { background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; }
  .panel h3 { color:#38bdf8; font-size:1rem; margin-bottom:16px; padding-bottom:10px; border-bottom:1px solid #334155; }
  .status-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #0f172a; font-size:0.85rem; }
  .status-row:last-child { border-bottom:none; }
  .status-label { color:#64748b; }
  table { width:100%; border-collapse:collapse; font-size:0.85rem; }
  th { background:#0f172a; color:#38bdf8; padding:10px 14px; text-align:left; font-weight:600; }
  td { padding:10px 14px; border-bottom:1px solid #1e293b; color:#cbd5e1; }
  .badge { padding:3px 10px; border-radius:10px; font-size:0.75rem; font-weight:bold; }
  .badge-motion { background:rgba(245,158,11,0.2); color:#f59e0b; }
  .badge-gas { background:rgba(239,68,68,0.2); color:#ef4444; }
  .badge-alarm { background:rgba(168,85,247,0.2); color:#a855f7; }
  .footer { text-align:center; padding:20px; color:#334155; font-size:0.75rem; }
  .ml-engine-badge { background:#1e293b; border:1px solid #2d3a4e; border-radius:8px; padding:10px; margin-top:12px; }
  .ml-engine-title { color:#38bdf8; font-size:0.9rem; font-weight:600; margin-bottom:8px; }
  .ml-engine-grid { display:grid; grid-template-columns:1fr 1fr; gap:4px 12px; font-size:0.8rem; }
  .ml-label { color:#64748b; }
  .ml-val { color:#e2e8f0; font-weight:600; }
  @media(max-width:900px) { .cards { grid-template-columns:repeat(2,1fr); } .charts { grid-template-columns:1fr; } }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>🏠 SentinelHome</h1>
    <div class="subtitle">Smart Home IoT Monitoring System — ML for IoT | UTM 2025/2026</div>
  </div>
  <div style="text-align:right">
    <div><span class="source-tag tag-local" id="sourceTag">LOCAL</span></div>
    <div style="color:#64748b;font-size:0.75rem;margin-top:4px">Last update: <span id="lastUpdate">--</span></div>
  </div>
</div>

<div class="container">

  <div class="controls">
    <div class="control-row">
      <span class="control-label">📡 Data Source</span>
      <button class="btn" id="btnSerial" onclick="setMode('serial')" title="USB Serial — XIAO must be connected via USB">🔌 USB Serial</button>
      <button class="btn active-local" id="btnLocal" onclick="setMode('local')" title="Local WiFi — laptop and XIAO on same hotspot">📶 Local Network</button>
      <button class="btn" id="btnSupabase" onclick="setMode('supabase')" title="Supabase cloud — works from anywhere">☁️ Supabase</button>
    </div>
    <div class="control-row">
      <span class="control-label">🌙 Night Mode</span>
      <div id="nightBtns">
        <button class="btn" id="btnDay" onclick="setNight('day')">☀️ Force Day</button>
        <button class="btn" id="btnNight" onclick="setNight('night')">🌑 Force Night</button>
        <button class="btn" id="btnAuto" onclick="setNight('auto')">🔄 Auto</button>
      </div>
      <span id="nightPhysicalMsg" style="font-size:0.8rem;color:#94a3b8;display:none">🔘 Use physical button on XIAO to toggle Day/Night mode</span>
    </div>
    <div class="control-row">
      <span class="control-label">☁️ XIAO → Supabase</span>
      <button class="btn" id="btnPushOn" onclick="setPush(true)">▶ Turn ON</button>
      <button class="btn" id="btnPushOff" onclick="setPush(false)">⏹ Turn OFF</button>
      <span style="font-size:0.75rem;color:#64748b;margin-left:4px">⚠ Requires Local Network</span>
    </div>
  </div>

  <div id="errorBanner" class="error-banner">
    <div class="err-title" id="errTitle"></div>
    <div id="errMessage"></div>
    <div class="err-action" id="errAction"></div>
  </div>

  <div id="warnBanner" class="warn-banner">
    <div id="warnMessage"></div>
  </div>

  <div class="cards">
    <div class="card">
      <div class="card-icon">🌡️</div>
      <div class="card-value" id="temp" style="color:#f87171">--</div>
      <div class="card-label">Temperature</div>
      <div class="card-status ok" id="tempStatus">--</div>
    </div>
    <div class="card">
      <div class="card-icon">💧</div>
      <div class="card-value" id="hum" style="color:#38bdf8">--</div>
      <div class="card-label">Humidity</div>
      <div class="card-status ok" id="humStatus">--</div>
    </div>
    <div class="card">
      <div class="card-icon">🚶</div>
      <div class="card-value" id="motion" style="color:#a78bfa">--</div>
      <div class="card-label">Motion (<span id="motionDur">0</span>s)</div>
      <div class="card-status ok" id="motionStatus">--</div>
    </div>
    <div class="card">
      <div class="card-icon">🔥</div>
      <div class="card-value" id="gas" style="color:#fb923c">--</div>
      <div class="card-label">Gas / Smoke</div>
      <div class="card-status ok" id="gasStatus">--</div>
    </div>
    <div class="card">
      <div class="card-icon">🚨</div>
      <div class="card-value" id="alarmclass" style="color:#f43f5e">--</div>
      <div class="card-label">Alert Class</div>
      <div class="card-status ok" id="reasonText">normal</div>
    </div>
  </div>

  <div class="charts">
    <div class="panel">
      <h3>📈 Temperature & Humidity — Last 50 Readings (Supabase)</h3>
      <canvas id="lineChart" height="100"></canvas>
    </div>
    <div class="panel">
      <h3>⚙️ System Status</h3>
      <div class="status-row"><span class="status-label">Data Source</span><strong id="sourceStatus">Local Network</strong></div>
      <div class="status-row"><span class="status-label">Night Mode</span><strong id="nightStatus">--</strong></div>
      <div class="status-row"><span class="status-label">XIAO Push</span><strong id="pushStatus">--</strong></div>
      <div class="status-row"><span class="status-label">Alert Class</span><strong id="classStatus">--</strong></div>
      <div class="status-row"><span class="status-label">Reason</span><strong id="reasonStatus">--</strong></div>
      <div class="status-row"><span class="status-label">Data Age</span><strong id="ageStatus">--</strong></div>
      <div class="status-row">
        <span class="status-label">ML Prediction</span>
        <strong id="mlClass">--</strong>
      </div>
      <div class="status-row">
        <span class="status-label">ML Confidence</span>
        <strong id="mlConf">--</strong>
      </div>
    </div>
    <div class="ml-engine-badge">
      <div class="ml-engine-title">⚡ Edge ML Engine</div>
      <div class="ml-engine-grid">
        <span class="ml-label">Model</span><span class="ml-val">Random Forest</span>
        <span class="ml-label">Trees</span><span class="ml-val">40</span>
        <span class="ml-label">Inference</span><span class="ml-val">On-device (XIAO)</span>
        <span class="ml-label">Features</span><span class="ml-val">6 sensor inputs</span>
        <span class="ml-label">Classes</span><span class="ml-val">4 alert levels</span>
        <span class="ml-label">Source</span><span class="ml-val" id="mlSourceBadge">—</span>
      </div>
    </div>
  </div>

  <div class="panel" style="margin-bottom:24px">
    <h3>⚠️ Alert Log — Recent Events</h3>
    <table>
      <thead><tr><th>Timestamp</th><th>Type</th><th>Class</th><th>Temp</th><th>Humidity</th><th>Reason</th></tr></thead>
      <tbody id="alertTable"><tr><td colspan="6" style="text-align:center;color:#334155">No alerts yet</td></tr></tbody>
    </table>
  </div>

</div>

<div class="footer">SentinelHome — ML IoT Group Project 2 | UTM 2025/2026 | 3-mode data source</div>

<script>
let lineChart;
let currentMode = "local";
const classColors = ['#22c55e','#fbbf24','#f97316','#ef4444'];
const classLabels = ['Normal','Comfort Alert','Warning','Danger'];

function initChart() {
  const ctx = document.getElementById('lineChart').getContext('2d');
  lineChart = new Chart(ctx, {
    type:'line',
    data:{ labels:[], datasets:[
      { label:'Temperature (°C)', data:[], borderColor:'#f87171', backgroundColor:'rgba(248,113,113,0.1)', tension:0.4, fill:true, pointRadius:2 },
      { label:'Humidity (%)', data:[], borderColor:'#38bdf8', backgroundColor:'rgba(56,189,248,0.1)', tension:0.4, fill:true, pointRadius:2 }
    ]},
    options:{ responsive:true, plugins:{ legend:{ labels:{ color:'#94a3b8' } } },
      scales:{ x:{ ticks:{ color:'#64748b', maxTicksLimit:8 }, grid:{ color:'#1e293b' } },
               y:{ ticks:{ color:'#64748b' }, grid:{ color:'#1e293b' } } } }
  });
}

function showError(title, message, action) {
  document.getElementById('errorBanner').classList.add('show');
  document.getElementById('warnBanner').classList.remove('show');
  document.getElementById('errTitle').textContent = '❌ ' + title;
  document.getElementById('errMessage').textContent = message;
  document.getElementById('errAction').textContent = action ? 'Next step: ' + action : '';
}
function showWarn(message) {
  document.getElementById('warnBanner').classList.add('show');
  document.getElementById('warnMessage').textContent = '⚠️ ' + message;
}
function hideError() {
  document.getElementById('errorBanner').classList.remove('show');
  document.getElementById('warnBanner').classList.remove('show');
}

function updateSourceUI(mode) {
  ['btnSerial','btnLocal','btnSupabase'].forEach(id => {
    document.getElementById(id).className = 'btn';
  });
  const map = { serial:'active-serial', local:'active-local', supabase:'active-supabase' };
  const tagMap = { serial:'🔌 USB SERIAL', local:'📶 LOCAL', supabase:'☁️ SUPABASE' };
  const tagClass = { serial:'tag-serial', local:'tag-local', supabase:'tag-supabase' };
  document.getElementById('btn' + mode.charAt(0).toUpperCase() + mode.slice(1)).classList.add(map[mode]);
  document.getElementById('sourceTag').textContent = tagMap[mode];
  document.getElementById('sourceTag').className = 'source-tag ' + tagClass[mode];
  document.getElementById('sourceStatus').textContent = tagMap[mode];

  // Show/hide night mode buttons based on mode
  const isLocal = (mode === 'local');
  document.getElementById('nightBtns').style.display = isLocal ? '' : 'none';
  document.getElementById('nightPhysicalMsg').style.display = isLocal ? 'none' : '';
}

async function setMode(mode) {
  currentMode = mode;
  updateSourceUI(mode);
  await fetch('/api/mode', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({mode}) });
  updateLatest();
}

async function setNight(action) {
  const btnMap = { day:'btnDay', night:'btnNight', auto:'btnAuto' };
  const clsMap = { day:'active-day', night:'active-night', auto:'active-auto' };
  ['btnDay','btnNight','btnAuto'].forEach(id => document.getElementById(id).className = 'btn');
  document.getElementById(btnMap[action]).classList.add(clsMap[action]);
  const r = await fetch('/api/night', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({action}) });
  const d = await r.json();
  if (!d.ok) showError('Night Mode Failed', d.message, d.action);
}

async function setPush(enabled) {
  document.getElementById('btnPushOn').className = 'btn' + (enabled ? ' active-on' : '');
  document.getElementById('btnPushOff').className = 'btn' + (!enabled ? ' active-off' : '');
  const r = await fetch('/api/supabase_push', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({enabled}) });
  const d = await r.json();
  if (!d.ok) showError('Push Toggle Failed', d.message, d.action);
  else document.getElementById('pushStatus').textContent = enabled ? 'ON ✅' : 'OFF ⏹';
}

async function updateLatest() {
  try {
    const d = await fetch('/api/latest').then(r => r.json());
    if (!d.ok) {
      showError(d.error || 'Error', d.message || '', d.action || '');
      return;
    }
    hideError();

    const t = d.temperature, h = d.humidity, m = d.motion, g = d.gas;
    const n = d.is_night, dur = d.motion_duration_sec || 0;
    const cls = d.alert_class || 0, reason = d.reason || 'normal';
    const mlCls = d.ml_class;
    const mlConf = d.ml_confidence;
    const push = d.xiao_push;
    const age = d.data_age_sec;

    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();

    document.getElementById('temp').textContent = t.toFixed(1) + '°C';
    const tEl = document.getElementById('tempStatus');
    tEl.textContent = t>=40?'DANGER':t>=35?'HOT':t>=30?'WARM':'Normal';
    tEl.className = 'card-status ' + (t>=40?'danger':t>=35?'danger':t>=30?'warn':'ok');

    document.getElementById('hum').textContent = h.toFixed(1) + '%';
    const hEl = document.getElementById('humStatus');
    hEl.textContent = h>=80?'CRITICAL':h>=70?'HIGH':'Normal';
    hEl.className = 'card-status ' + (h>=80?'danger':h>=70?'warn':'ok');

    document.getElementById('motion').textContent = m ? 'YES' : 'NO';
    document.getElementById('motionDur').textContent = dur;
    const mEl = document.getElementById('motionStatus');
    mEl.textContent = m ? (dur+'s detected') : 'Clear';
    mEl.className = 'card-status ' + (m ? 'warn' : 'ok');

    document.getElementById('gas').textContent = g ? 'YES' : 'NO';
    const gEl = document.getElementById('gasStatus');
    gEl.textContent = g ? 'GAS ALERT' : 'Safe';
    gEl.className = 'card-status ' + (g ? 'danger' : 'ok');

    document.getElementById('alarmclass').textContent = cls;
    document.getElementById('alarmclass').style.color = classColors[cls] || '#f43f5e';
    const rEl = document.getElementById('reasonText');
    rEl.textContent = classLabels[cls] || 'Unknown';
    rEl.className = 'card-status ' + (['ok','warn','warn','danger'][cls]);

    document.getElementById('nightStatus').textContent = n ? '🌑 Night' : '☀️ Day';
    if (push !== undefined) document.getElementById('pushStatus').textContent = push ? 'ON ✅' : 'OFF ⏹';
    document.getElementById('classStatus').textContent = cls + ' — ' + classLabels[cls];
    document.getElementById('reasonStatus').textContent = reason.replace(/_/g,' ');
    document.getElementById('ageStatus').textContent = age !== undefined ? age+'s ago' : '--';

    const classLabelsML = ['Normal','Low Alert','Medium Alert','High Alert'];
    if (mlCls !== null && mlCls !== undefined) {
      document.getElementById('mlClass').textContent = mlCls + ' — ' + (classLabelsML[mlCls] || 'Unknown');
      document.getElementById('mlClass').style.color = classColors[mlCls] || '#e2e8f0';
      document.getElementById('mlConf').textContent = mlConf ? (mlConf * 100).toFixed(1) + '%' : '--';
    }

    const src = d.ml_source || "—";
    const srcEl = document.getElementById("mlSourceBadge");
    if (srcEl) {
      srcEl.textContent = src === "xiao" ? "XIAO TinyML ✅" : src === "flask" ? "Flask fallback" : "—";
      srcEl.style.color = src === "xiao" ? "#4ade80" : src === "flask" ? "#facc15" : "#94a3b8";
    }

    if (d.stale_warning) showWarn(d.stale_warning);

  } catch(e) { console.error(e); }
}

async function updateHistory() {
  try {
    const rows = await fetch('/api/history').then(r => r.json());
    if (!rows.length) return;
    const labels = rows.map(r => new Date(r.created_at).toLocaleTimeString()).reverse();
    const temps = rows.map(r => r.temperature).reverse();
    const hums = rows.map(r => r.humidity).reverse();
    lineChart.data.labels = labels;
    lineChart.data.datasets[0].data = temps;
    lineChart.data.datasets[1].data = hums;
    lineChart.update();
  } catch(e) { console.error(e); }
}

async function updateAlerts() {
  try {
    const rows = await fetch('/api/alerts').then(r => r.json());
    const tbody = document.getElementById('alertTable');
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#334155">No alerts yet</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => {
      const types = [];
      if (r.motion) types.push('<span class="badge badge-motion">MOTION</span>');
      if (r.gas) types.push('<span class="badge badge-gas">GAS</span>');
      if (r.alarm) types.push('<span class="badge badge-alarm">ALARM</span>');
      const cls = r.alert_class || 0;
      return `<tr>
        <td>${new Date(r.created_at).toLocaleString()}</td>
        <td>${types.join(' ')}</td>
        <td style="color:${classColors[cls]};font-weight:bold">Class ${cls}</td>
        <td>${r.temperature?.toFixed(1)}°C</td>
        <td>${r.humidity?.toFixed(1)}%</td>
        <td>${(r.reason||'').replace(/_/g,' ')}</td>
      </tr>`;
    }).join('');
  } catch(e) { console.error(e); }
}

let historyTimer = 0;
async function refresh() {
  await updateLatest();
  historyTimer++;
  if (historyTimer >= 10) {
    await updateHistory();
    await updateAlerts();
    historyTimer = 0;
  }
}

initChart();
refresh();
setInterval(refresh, 1000);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("SentinelHome Dashboard — 3-mode data source")
    print("  🔌 USB Serial  — XIAO via USB cable, no WiFi needed")
    print("  📶 Local Network — XIAO via WiFi, same hotspot required")
    print("  ☁️  Supabase   — cloud data, works anywhere")
    print("Open: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)