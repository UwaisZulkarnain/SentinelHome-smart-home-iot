from flask import Flask, render_template_string, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

XIAO_IP = "172.20.10.2"
XIAO_URL = f"http://{XIAO_IP}/data"
SUPABASE_URL = "https://ubcyktzfiylqirzpdqnu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViY3lrdHpmaXlscWlyenBkcW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4MDkxNjQsImV4cCI6MjA5NzM4NTE2NH0.Gu0jBFdVnsBMFF2VWliTnoKtBqCt_-IwSQfnoe2ts9c"

HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/latest")
def latest():
    # Try XIAO directly first (instant)
    try:
        r = requests.get(XIAO_URL, timeout=2)
        d = r.json()
        return jsonify({
            "temperature": d.get("t", 0),
            "humidity": d.get("h", 0),
            "motion": d.get("m", 0),
            "gas": d.get("g", 0),
            "alarm": d.get("a", 0),
            "created_at": datetime.utcnow().isoformat(),
            "source": "xiao"
        })
    except:
        pass
    # Fallback to Supabase (remote users)
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=1",
            headers=HEADERS
        )
        data = r.json()
        if data:
            data[0]["source"] = "supabase"
            return jsonify(data[0])
    except:
        pass
    return jsonify({})

@app.route("/api/history")
def history():
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=50",
            headers=HEADERS
        )
        return jsonify(r.json())
    except:
        return jsonify([])

@app.route("/api/alerts")
def alerts():
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.desc&limit=100",
            headers=HEADERS
        )
        rows = r.json()
        return jsonify([row for row in rows if row.get("motion") or row.get("gas") or row.get("alarm")][:20])
    except:
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
  body { font-family:'Segoe UI',sans-serif; background:#0a0e1a; color:#e2e8f0; min-height:100vh; }
  .header {
    background: linear-gradient(135deg, #1e3a5f, #0f2027);
    padding: 20px 30px; display:flex; align-items:center;
    justify-content:space-between; border-bottom:1px solid #1e3a5f;
  }
  .header h1 { font-size:1.6rem; color:#38bdf8; letter-spacing:2px; }
  .header .subtitle { font-size:0.8rem; color:#64748b; margin-top:4px; }
  .live-dot { width:10px; height:10px; background:#22c55e; border-radius:50%;
    display:inline-block; margin-right:6px; animation:blink 1s infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
  .source-badge { font-size:0.7rem; padding:2px 8px; border-radius:8px; margin-left:8px; }
  .source-xiao { background:rgba(56,189,248,0.2); color:#38bdf8; }
  .source-supabase { background:rgba(168,85,247,0.2); color:#a855f7; }
  .alert-banner {
    background:#dc2626; color:white; text-align:center;
    padding:12px; font-weight:bold; font-size:1rem;
    display:none; animation:pulse 1s infinite;
  }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }
  .container { max-width:1400px; margin:0 auto; padding:24px; }
  .cards { display:grid; grid-template-columns:repeat(5,1fr); gap:16px; margin-bottom:24px; }
  .card {
    background:#1e293b; border-radius:12px; padding:20px;
    border:1px solid #334155; text-align:center; transition:transform 0.2s;
  }
  .card:hover { transform:translateY(-3px); }
  .card-icon { font-size:2rem; margin-bottom:8px; }
  .card-value { font-size:2.2rem; font-weight:700; margin:6px 0; }
  .card-label { font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; }
  .card-status { font-size:0.75rem; font-weight:600; padding:3px 10px; border-radius:10px; display:inline-block; margin-top:6px; }
  .ok { background:rgba(34,197,94,0.15); color:#22c55e; }
  .warn { background:rgba(245,158,11,0.15); color:#f59e0b; }
  .danger { background:rgba(239,68,68,0.15); color:#ef4444; }
  .charts { display:grid; grid-template-columns:2fr 1fr; gap:16px; margin-bottom:24px; }
  .panel { background:#1e293b; border-radius:12px; padding:20px; border:1px solid #334155; }
  .panel h3 { color:#38bdf8; font-size:1rem; margin-bottom:16px; padding-bottom:10px; border-bottom:1px solid #334155; }
  .alert-log { margin-bottom:24px; }
  table { width:100%; border-collapse:collapse; font-size:0.85rem; }
  th { background:#0f172a; color:#38bdf8; padding:10px 14px; text-align:left; font-weight:600; }
  td { padding:10px 14px; border-bottom:1px solid #1e293b; color:#cbd5e1; }
  tr:hover td { background:#1e293b; }
  .badge { padding:3px 10px; border-radius:10px; font-size:0.75rem; font-weight:bold; }
  .badge-motion { background:rgba(245,158,11,0.2); color:#f59e0b; }
  .badge-gas { background:rgba(239,68,68,0.2); color:#ef4444; }
  .badge-alarm { background:rgba(168,85,247,0.2); color:#a855f7; }
  .footer { text-align:center; padding:20px; color:#334155; font-size:0.75rem; border-top:1px solid #1e293b; }
  .stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .stat-box { background:#0f172a; border-radius:8px; padding:14px; text-align:center; }
  .stat-val { font-size:1.6rem; font-weight:700; color:#38bdf8; }
  .stat-label { font-size:0.7rem; color:#64748b; margin-top:4px; text-transform:uppercase; }
  @media(max-width:900px) {
    .cards { grid-template-columns:repeat(2,1fr); }
    .charts { grid-template-columns:1fr; }
  }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>🏠 SentinelHome</h1>
    <div class="subtitle">Smart Home IoT Monitoring System</div>
  </div>
  <div style="text-align:right">
    <div>
      <span class="live-dot"></span>
      <span style="color:#22c55e;font-size:0.85rem">LIVE</span>
      <span class="source-badge" id="sourceBadge">--</span>
    </div>
    <div style="color:#64748b;font-size:0.75rem;margin-top:4px">
      Last update: <span id="lastUpdate">--</span>
    </div>
  </div>
</div>

<div id="alertBanner" class="alert-banner">⚠️ ALERT DETECTED — CHECK SENSORS</div>

<div class="container">
  <div class="cards">
    <div class="card">
      <div class="card-icon">🌡️</div>
      <div class="card-value" id="temp" style="color:#f87171">--</div>
      <div class="card-label">Temperature</div>
      <div class="card-status ok" id="tempStatus">Normal</div>
    </div>
    <div class="card">
      <div class="card-icon">💧</div>
      <div class="card-value" id="hum" style="color:#38bdf8">--</div>
      <div class="card-label">Humidity</div>
      <div class="card-status ok" id="humStatus">Normal</div>
    </div>
    <div class="card">
      <div class="card-icon">🚶</div>
      <div class="card-value" id="motion" style="color:#a78bfa">--</div>
      <div class="card-label">Motion</div>
      <div class="card-status ok" id="motionStatus">Clear</div>
    </div>
    <div class="card">
      <div class="card-icon">🔥</div>
      <div class="card-value" id="gas" style="color:#fb923c">--</div>
      <div class="card-label">Gas / Smoke</div>
      <div class="card-status ok" id="gasStatus">Safe</div>
    </div>
    <div class="card">
      <div class="card-icon">🚨</div>
      <div class="card-value" id="alarm" style="color:#f43f5e">--</div>
      <div class="card-label">Alarm</div>
      <div class="card-status ok" id="alarmStatus">Off</div>
    </div>
  </div>

  <div class="charts">
    <div class="panel">
      <h3>📈 Temperature & Humidity — Last 50 Readings</h3>
      <canvas id="lineChart" height="100"></canvas>
    </div>
    <div class="panel">
      <h3>📊 Session Stats</h3>
      <div class="stats-grid">
        <div class="stat-box"><div class="stat-val" id="statAvgTemp">--</div><div class="stat-label">Avg Temp °C</div></div>
        <div class="stat-box"><div class="stat-val" id="statAvgHum">--</div><div class="stat-label">Avg Humidity %</div></div>
        <div class="stat-box"><div class="stat-val" id="statMotionCount">--</div><div class="stat-label">Motion Events</div></div>
        <div class="stat-box"><div class="stat-val" id="statGasCount">--</div><div class="stat-label">Gas Events</div></div>
        <div class="stat-box"><div class="stat-val" id="statMaxTemp">--</div><div class="stat-label">Max Temp °C</div></div>
        <div class="stat-box"><div class="stat-val" id="statTotalRows">--</div><div class="stat-label">Total Readings</div></div>
      </div>
    </div>
  </div>

  <div class="panel alert-log">
    <h3>⚠️ Alert Log — Recent Events</h3>
    <table>
      <thead>
        <tr><th>Timestamp</th><th>Type</th><th>Temperature</th><th>Humidity</th><th>Details</th></tr>
      </thead>
      <tbody id="alertTable">
        <tr><td colspan="5" style="text-align:center;color:#334155">No alerts yet</td></tr>
      </tbody>
    </table>
  </div>
</div>

<div class="footer">
  SentinelHome — ML IoT Group Project 2 | UTM 2025/2026
</div>

<script>
let lineChart;

function initChart() {
  const ctx = document.getElementById('lineChart').getContext('2d');
  lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        { label:'Temperature (°C)', data:[], borderColor:'#f87171',
          backgroundColor:'rgba(248,113,113,0.1)', tension:0.4, fill:true, pointRadius:2 },
        { label:'Humidity (%)', data:[], borderColor:'#38bdf8',
          backgroundColor:'rgba(56,189,248,0.1)', tension:0.4, fill:true, pointRadius:2 }
      ]
    },
    options: {
      responsive:true,
      plugins:{ legend:{ labels:{ color:'#94a3b8' } } },
      scales:{
        x:{ ticks:{ color:'#64748b', maxTicksLimit:8 }, grid:{ color:'#1e293b' } },
        y:{ ticks:{ color:'#64748b' }, grid:{ color:'#1e293b' } }
      }
    }
  });
}

function setCard(id, value, statusId, statusText, cls) {
  document.getElementById(id).textContent = value;
  const s = document.getElementById(statusId);
  s.textContent = statusText;
  s.className = 'card-status ' + cls;
}

async function updateLatest() {
  try {
    const d = await fetch('/api/latest').then(r => r.json());
    if (!d || d.temperature === undefined) return;

    const t = d.temperature, h = d.humidity;
    const m = d.motion, g = d.gas, a = d.alarm;

    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();

    const badge = document.getElementById('sourceBadge');
    if (d.source === 'xiao') {
      badge.textContent = '⚡ XIAO Direct';
      badge.className = 'source-badge source-xiao';
    } else {
      badge.textContent = '☁️ Supabase';
      badge.className = 'source-badge source-supabase';
    }

    setCard('temp', t.toFixed(1)+'°C', 'tempStatus', t>35?'HIGH':'Normal', t>35?'danger':'ok');
    setCard('hum', h.toFixed(1)+'%', 'humStatus', h>80?'HIGH':'Normal', h>80?'warn':'ok');
    setCard('motion', m?'YES':'NO', 'motionStatus', m?'DETECTED':'Clear', m?'warn':'ok');
    setCard('gas', g?'YES':'NO', 'gasStatus', g?'DETECTED':'Safe', g?'danger':'ok');
    setCard('alarm', a?'ON':'OFF', 'alarmStatus', a?'ACTIVE':'Standby', a?'danger':'ok');

    document.getElementById('alertBanner').style.display =
      (m || g || a || t>35 || h>80) ? 'block' : 'none';

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

    document.getElementById('statAvgTemp').textContent = (temps.reduce((a,b)=>a+b,0)/temps.length).toFixed(1);
    document.getElementById('statAvgHum').textContent = (hums.reduce((a,b)=>a+b,0)/hums.length).toFixed(1);
    document.getElementById('statMaxTemp').textContent = Math.max(...temps).toFixed(1);
    document.getElementById('statMotionCount').textContent = rows.filter(r=>r.motion).length;
    document.getElementById('statGasCount').textContent = rows.filter(r=>r.gas).length;
    document.getElementById('statTotalRows').textContent = rows.length;
  } catch(e) { console.error(e); }
}

async function updateAlerts() {
  try {
    const rows = await fetch('/api/alerts').then(r => r.json());
    const tbody = document.getElementById('alertTable');
    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:#334155">No alerts yet</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => {
      const types = [];
      if (r.motion) types.push('<span class="badge badge-motion">MOTION</span>');
      if (r.gas) types.push('<span class="badge badge-gas">GAS</span>');
      if (r.alarm) types.push('<span class="badge badge-alarm">ALARM</span>');
      return `<tr>
        <td>${new Date(r.created_at).toLocaleString()}</td>
        <td>${types.join(' ')}</td>
        <td>${r.temperature?.toFixed(1)}°C</td>
        <td>${r.humidity?.toFixed(1)}%</td>
        <td>T:${r.temperature?.toFixed(1)} H:${r.humidity?.toFixed(1)} M:${r.motion} G:${r.gas}</td>
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
    print("SentinelHome Dashboard")
    print("Live cards: XIAO direct (instant) with Supabase fallback")
    print("History/alerts: Supabase (every 10s)")
    print("Open: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)