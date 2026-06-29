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
import pygame
import threading
tts_available = False
tts_last_played = {1: 0, 2: 0, 3: 0}
tts_last_class = 0

def init_tts():
    global tts_available
    try:
        pygame.mixer.init()
        tts_available = True
        print("[TTS] Audio ready")
    except Exception as e:
        print(f"[TTS] Audio unavailable: {e}")

def speak_alert(alert_class):
    global tts_last_class, tts_last_played
    if not tts_available:
        return
    if alert_class == 0:
        tts_last_class = 0
        return

    now = time.time()

    # Repeat intervals per class
    repeat_interval = {1: 999999, 2: 30, 3: 10}

    # Play if class changed OR repeat interval passed
    class_changed = (alert_class != tts_last_class)
    interval_passed = (now - tts_last_played.get(alert_class, 0)) >= repeat_interval[alert_class]

    if not (class_changed or interval_passed):
        return

    tts_last_class = alert_class
    tts_last_played[alert_class] = now

    def play():
        try:
            for lang in ['bm', 'en']:
                path = f"warnings/class{alert_class}_{lang}.mp3"
                if os.path.exists(path):
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    time.sleep(0.4)
        except Exception as e:
            print(f"[TTS Error] {e}")

    threading.Thread(target=play, daemon=True).start()

app = Flask(__name__)

XIAO_IP = "172.20.10.2"
XIAO_URL = f"http://{XIAO_IP}/data"
SUPABASE_URL = "https://ubcyktzfiylqirzpdqnu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViY3lrdHpmaXlscWlyenBkcW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4MDkxNjQsImV4cCI6MjA5NzM4NTE2NH0.Gu0jBFdVnsBMFF2VWliTnoKtBqCt_-IwSQfnoe2ts9c"
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
SERIAL_PORT = "COM10"
SERIAL_BAUD = 115200

MODEL_PATH = "ML\\new_random_forest_model_n70.pkl"
SCALER_PATH = "ML\\scaler_n70.pkl"

ml_model = None
ml_scaler = None

try:
    ml_model = joblib.load(MODEL_PATH)
    ml_scaler = joblib.load(SCALER_PATH)
    print("ML model loaded successfully")
except Exception as e:
    print(f"ML model not loaded: {e}")

init_tts()

# ml_predict disabled — ML inference runs on XIAO TinyML directly
def ml_predict(temperature, humidity, motion, gas, is_night, motion_duration_sec):
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
        result["ml_source"] = "xiao" if result.get("ml_class") is not None else "none"
        speak_alert(int(result.get("alert_class", 0) or 0))
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
            data["ml_source"] = "xiao" if data.get("ml_class") is not None else "none"
            speak_alert(int(data.get("alert_class", 0) or 0))
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
            row["ml_source"] = "xiao" if row.get("ml_class") is not None else "none"
            speak_alert(int(row.get("alert_class", 0) or 0))
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

@app.route("/api/tts_status")
def tts_status():
    cls = tts_last_class
    messages = {
        0: None,
        1: {"bm": "Perhatian. Keadaan tidak selesa dikesan. Sila semak persekitaran anda.", "en": "Attention. Comfort alert detected. Please check your environment."},
        2: {"bm": "Amaran. Situasi membimbangkan dikesan. Sila ambil tindakan segera.", "en": "Warning. Concerning situation detected. Please take action immediately."},
        3: {"bm": "Bahaya! Keadaan berbahaya dikesan! Sila keluar dari kawasan ini sekarang!", "en": "Danger! Hazardous condition detected! Please evacuate the area immediately!"}
    }
    return jsonify({"alert_class": cls, "message": messages.get(cls)})

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SentinelHome Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  :root {
    --bg:#070b14; --panel:#0f1729; --panel-2:#131d33; --line:#1f2c44;
    --text:#e6edf7; --muted:#7a8aa3; --dim:#4a5872;
    --accent:#38bdf8; --accent-2:#818cf8;
    --ok:#22c55e; --warn:#f59e0b; --danger:#ef4444;
    --radius:16px;
  }
  body {
    font-family:'Inter',-apple-system,'Segoe UI',sans-serif;
    background:
      radial-gradient(900px 500px at 12% -8%, rgba(56,189,248,0.10), transparent 60%),
      radial-gradient(800px 500px at 100% 0%, rgba(129,140,248,0.10), transparent 55%),
      var(--bg);
    background-attachment:fixed;
    color:var(--text); min-height:100vh; font-size:16px;
    -webkit-font-smoothing:antialiased; letter-spacing:0.1px;
  }
  .header {
    background:linear-gradient(135deg, rgba(30,58,95,0.55), rgba(15,32,39,0.35));
    backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
    padding:22px 40px; display:flex; align-items:center; justify-content:space-between;
    border-bottom:1px solid var(--line);
    position:sticky; top:0; z-index:50;
  }
  .header h1 {
    font-size:2rem; font-weight:800; letter-spacing:1.5px;
    background:linear-gradient(90deg,#7dd3fc,#a5b4fc);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
  }
  .header .subtitle { font-size:0.9rem; color:var(--muted); margin-top:6px; font-weight:500; }
  .container { max-width:1480px; margin:0 auto; padding:32px 40px; }
  .controls {
    background:linear-gradient(180deg, var(--panel-2), var(--panel));
    border-radius:var(--radius); padding:22px 24px; margin-bottom:24px;
    border:1px solid var(--line); box-shadow:0 10px 40px -20px rgba(0,0,0,0.8);
  }
  .control-row { display:flex; align-items:center; gap:14px; margin-bottom:16px; flex-wrap:wrap; }
  .control-row:last-child { margin-bottom:0; }
  .control-label { font-size:0.92rem; color:var(--muted); min-width:160px; font-weight:700; letter-spacing:0.3px; }
  .btn {
    background:rgba(255,255,255,0.04); color:var(--text);
    border:1px solid rgba(255,255,255,0.08); padding:10px 18px; border-radius:11px;
    cursor:pointer; font-size:0.9rem; font-weight:600; font-family:inherit;
    transition:transform .12s ease, background .15s, border-color .15s, box-shadow .15s;
  }
  .btn:hover { background:rgba(255,255,255,0.09); border-color:rgba(255,255,255,0.18); transform:translateY(-1px); }
  .btn:active { transform:translateY(0); }
  .btn.active-serial { background:var(--warn); color:#0a0e1a; border-color:transparent; box-shadow:0 0 22px -4px rgba(245,158,11,0.6); }
  .btn.active-local { background:var(--accent); color:#0a0e1a; border-color:transparent; box-shadow:0 0 22px -4px rgba(56,189,248,0.6); }
  .btn.active-supabase { background:var(--accent-2); color:#0a0e1a; border-color:transparent; box-shadow:0 0 22px -4px rgba(129,140,248,0.6); }
  .btn.active-night { background:#6366f1; color:#fff; border-color:transparent; }
  .btn.active-day { background:#fbbf24; color:#0a0e1a; border-color:transparent; }
  .btn.active-auto { background:var(--ok); color:#0a0e1a; border-color:transparent; }
  .btn.active-on { background:var(--ok); color:#0a0e1a; border-color:transparent; }
  .btn.active-off { background:var(--danger); color:#fff; border-color:transparent; }
  .source-tag { font-size:0.78rem; padding:4px 14px; border-radius:999px; font-weight:700; letter-spacing:0.5px; }
  .tag-serial { background:rgba(245,158,11,0.18); color:var(--warn); border:1px solid rgba(245,158,11,0.3); }
  .tag-local { background:rgba(56,189,248,0.18); color:var(--accent); border:1px solid rgba(56,189,248,0.3); }
  .tag-supabase { background:rgba(129,140,248,0.18); color:var(--accent-2); border:1px solid rgba(129,140,248,0.3); }
  .error-banner { background:linear-gradient(180deg,#5b1414,#3f0d0d); border:1px solid rgba(239,68,68,0.5); color:#fecaca;
    padding:16px 20px; border-radius:13px; margin-bottom:22px; display:none; }
  .error-banner.show { display:block; }
  .warn-banner { background:linear-gradient(180deg,#5e2c0a,#3f1e06); border:1px solid rgba(245,158,11,0.5); color:#fde68a;
    padding:12px 20px; border-radius:13px; margin-bottom:22px; display:none; }
  .warn-banner.show { display:block; }
  .err-title { font-weight:700; margin-bottom:5px; font-size:1.02rem; }
  .err-action { font-size:0.9rem; margin-top:7px; opacity:0.88; }
  .cards { display:grid; grid-template-columns:repeat(5,1fr); gap:18px; margin-bottom:26px; }
  .card {
    background:linear-gradient(180deg, var(--panel-2), var(--panel));
    border-radius:var(--radius); padding:24px 18px; border:1px solid var(--line);
    text-align:center; position:relative; overflow:hidden;
    transition:transform .15s ease, border-color .15s;
  }
  .card::before {
    content:''; position:absolute; inset:0 0 auto 0; height:3px;
    background:linear-gradient(90deg, transparent, var(--accent), transparent); opacity:0.5;
  }
  .card:hover { transform:translateY(-3px); border-color:rgba(56,189,248,0.35); }
  .card-icon { font-size:2.3rem; margin-bottom:10px; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.4)); }
  .card-value { font-size:2.5rem; font-weight:800; margin:6px 0; line-height:1.05; letter-spacing:-0.5px; }
  .card-label { font-size:0.8rem; color:var(--dim); text-transform:uppercase; letter-spacing:1.5px; font-weight:600; }
  .card-status { font-size:0.82rem; font-weight:700; padding:4px 13px; border-radius:999px; display:inline-block; margin-top:10px; }
  .ok { background:rgba(34,197,94,0.16); color:var(--ok); }
  .warn { background:rgba(245,158,11,0.16); color:var(--warn); }
  .danger { background:rgba(239,68,68,0.16); color:var(--danger); }
  .charts { display:grid; grid-template-columns:2fr 1fr; gap:18px; margin-bottom:26px; }
  .panel {
    background:linear-gradient(180deg, var(--panel-2), var(--panel));
    border-radius:var(--radius); padding:24px; border:1px solid var(--line);
    box-shadow:0 10px 40px -24px rgba(0,0,0,0.9);
  }
  .panel h3 { color:var(--accent); font-size:1.08rem; font-weight:700; margin-bottom:18px; padding-bottom:12px; border-bottom:1px solid var(--line); letter-spacing:0.3px; }
  .status-row { display:flex; justify-content:space-between; align-items:center; padding:11px 0; border-bottom:1px solid rgba(31,44,68,0.6); font-size:0.92rem; }
  .status-row:last-child { border-bottom:none; }
  .status-label { color:var(--muted); font-weight:500; }
  .status-row strong { font-weight:700; }
  table { width:100%; border-collapse:collapse; font-size:0.9rem; }
  th { background:rgba(15,23,41,0.8); color:var(--accent); padding:12px 16px; text-align:left; font-weight:700; letter-spacing:0.4px; text-transform:uppercase; font-size:0.78rem; }
  th:first-child { border-radius:10px 0 0 10px; }
  th:last-child { border-radius:0 10px 10px 0; }
  td { padding:12px 16px; border-bottom:1px solid rgba(31,44,68,0.5); color:#c2cfe2; }
  tr:hover td { background:rgba(56,189,248,0.04); }
  .badge { padding:4px 12px; border-radius:999px; font-size:0.76rem; font-weight:700; letter-spacing:0.3px; }
  .badge-motion { background:rgba(245,158,11,0.2); color:var(--warn); }
  .badge-gas { background:rgba(239,68,68,0.2); color:var(--danger); }
  .badge-alarm { background:rgba(168,85,247,0.2); color:#c084fc; }
  .footer { text-align:center; padding:26px; color:var(--dim); font-size:0.82rem; letter-spacing:0.5px; }
  .ml-engine-badge {
    background:linear-gradient(180deg, var(--panel-2), var(--panel));
    border:1px solid var(--line); border-radius:var(--radius); padding:18px 20px; margin-top:0;
  }
  .ml-engine-title { color:var(--accent); font-size:1rem; font-weight:700; margin-bottom:14px; letter-spacing:0.3px; }
  .ml-engine-grid { display:grid; grid-template-columns:1fr 1fr; gap:9px 16px; font-size:0.88rem; }
  .ml-label { color:var(--muted); font-weight:500; }
  .ml-val { color:var(--text); font-weight:700; font-family:'JetBrains Mono',monospace; }
  .container { max-width:1280px; margin:0 auto; padding:24px 32px; }
  .tts-banner {
    display:none; align-items:center; gap:14px;
    background:linear-gradient(135deg, rgba(239,68,68,0.15), rgba(245,158,11,0.10));
    border:1px solid rgba(239,68,68,0.4); border-radius:13px;
    padding:14px 20px; margin-bottom:20px;
    animation: pulse-border 1.5s ease-in-out infinite;
  }
  .tts-banner.show { display:flex; }
  .tts-icon { font-size:1.6rem; flex-shrink:0; }
  .tts-text { flex:1; }
  .tts-label { font-size:0.75rem; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:3px; }
  .tts-bm { font-size:1rem; font-weight:700; color:#fde68a; margin-bottom:2px; }
  .tts-en { font-size:0.88rem; color:#fca5a5; font-weight:500; }
  .tts-class-badge { font-size:0.78rem; font-weight:800; padding:5px 14px; border-radius:999px; flex-shrink:0; }
  @keyframes pulse-border { 0%,100% { border-color:rgba(239,68,68,0.4); } 50% { border-color:rgba(239,68,68,0.9); } }
  @media(max-width:1100px) { .cards { grid-template-columns:repeat(3,1fr); } .charts { grid-template-columns:1fr; } }
  @media(max-width:680px) { .cards { grid-template-columns:repeat(2,1fr); } .container { padding:20px; } }
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

  <div id="ttsBanner" class="tts-banner">
    <div class="tts-icon" id="ttsIcon">🔊</div>
    <div class="tts-text">
      <div class="tts-label">🔊 Voice Alert Broadcasting</div>
      <div class="tts-bm" id="ttsBm">--</div>
      <div class="tts-en" id="ttsEn">--</div>
    </div>
    <span class="tts-class-badge" id="ttsClassBadge">--</span>
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

const ttsMessages = {
  1: { bm: "Perhatian. Keadaan tidak selesa dikesan. Sila semak persekitaran anda.", en: "Attention. Comfort alert detected. Please check your environment." },
  2: { bm: "Amaran. Situasi membimbangkan dikesan. Sila ambil tindakan segera.", en: "Warning. Concerning situation detected. Please take action immediately." },
  3: { bm: "Bahaya! Keadaan berbahaya dikesan! Sila keluar dari kawasan ini sekarang!", en: "Danger! Hazardous condition detected! Please evacuate the area immediately!" }
};
const ttsBadgeColors = { 1:'#fbbf24', 2:'#f97316', 3:'#ef4444' };
const ttsBadgeLabels = { 1:'CLASS 1', 2:'CLASS 2', 3:'CLASS 3' };

async function updateTTS() {
  try {
    const d = await fetch('/api/tts_status').then(r => r.json());
    const cls = d.alert_class;
    const banner = document.getElementById('ttsBanner');
    if (cls && cls > 0 && ttsMessages[cls]) {
      document.getElementById('ttsBm').textContent = ttsMessages[cls].bm;
      document.getElementById('ttsEn').textContent = ttsMessages[cls].en;
      const badge = document.getElementById('ttsClassBadge');
      badge.textContent = ttsBadgeLabels[cls];
      badge.style.background = ttsBadgeColors[cls] + '33';
      badge.style.color = ttsBadgeColors[cls];
      banner.classList.add('show');
    } else {
      banner.classList.remove('show');
    }
  } catch(e) {}
}
setInterval(updateTTS, 1500);
updateTTS();
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