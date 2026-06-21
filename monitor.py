import serial
import os
import time
from datetime import datetime

PORT = "COM10"
BAUD = 115200

def clear():
    os.system('cls')

print("Connecting to XIAO on", PORT)
ser = serial.Serial(PORT, BAUD, timeout=2)
time.sleep(2)

data = {"t": 0, "h": 0, "m": 0, "g": 0, "a": 0, "n": 0, "dur": 0, "cls": 0, "reason": "normal"}

while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if line.startswith("T:"):
            tokens = line.split()
            d = {}
            for tok in tokens:
                k, v = tok.split(":", 1)
                d[k] = v
            data = {
                "t": float(d.get("T", 0)),
                "h": float(d.get("H", 0)),
                "m": int(d.get("M", 0)),
                "g": int(d.get("G", 0)),
                "a": int(d.get("A", 0)),
                "n": int(d.get("N", 0)),
                "dur": int(d.get("DUR", 0)),
                "cls": int(d.get("CLASS", 0)),
                "reason": d.get("REASON", "normal")
            }

        clear()
        now = datetime.now().strftime("%H:%M:%S")
        t, h, m, g, a = data["t"], data["h"], data["m"], data["g"], data["a"]
        n, dur, cls, reason = data["n"], data["dur"], data["cls"], data["reason"]

        print("╔══════════════════════════════════════════╗")
        print("║      🏠 SentinelHome Live Monitor         ║")
        print(f"║               {now}                ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║  🌡  Temp      : {t:.1f}°C  {'⚠ HIGH' if t > 35 else '✅ OK   '}               ║")
        print(f"║  💧 Humidity  : {h:.1f}%   {'⚠ HIGH' if h > 80 else '✅ OK   '}               ║")
        print(f"║  🚶 Motion    : {'🔴 DETECTED    ' if m else '🟢 Clear       '}  DUR:{dur}s        ║")
        print(f"║  🔥 Gas/Smoke : {'🔴 DETECTED    ' if g else '🟢 Clear       '}               ║")
        print(f"║  🚨 Alarm     : {'🔴 ACTIVE      ' if a else '🟢 Off         '}               ║")
        print(f"║  🌙 Night Mode: {'🌑 ON ' if n else '☀️  OFF'}                           ║")
        print(f"║  📊 Class     : {cls} — {reason:<30}║")
        print("╚══════════════════════════════════════════╝")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)