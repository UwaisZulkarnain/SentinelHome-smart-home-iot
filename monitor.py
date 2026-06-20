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

data = {"t": 0, "h": 0, "m": 0, "g": 0, "a": 0}

while True:
    try:
        line = ser.readline().decode().strip()
        if line.startswith("T:"):
            parts = line.replace("T:","").replace("H:","").replace("M:","").replace("G:","").replace("A:","").split()
            if len(parts) == 5:
                data = {
                    "t": float(parts[0]),
                    "h": float(parts[1]),
                    "m": int(parts[2]),
                    "g": int(parts[3]),
                    "a": int(parts[4])
                }
        
        clear()
        now = datetime.now().strftime("%H:%M:%S")
        t, h, m, g, a = data["t"], data["h"], data["m"], data["g"], data["a"]
        
        print("╔══════════════════════════════════════╗")
        print("║     🏠 SentinelHome Live Monitor      ║")
        print(f"║              {now}               ║")
        print("╠══════════════════════════════════════╣")
        print(f"║  🌡  Temp      : {t:.1f}°C  {'⚠ HIGH' if t > 35 else '✅ OK   '}              ║")
        print(f"║  💧 Humidity  : {h:.1f}%   {'⚠ HIGH' if h > 80 else '✅ OK   '}              ║")
        print(f"║  🚶 Motion    : {'🔴 DETECTED    ' if m else '🟢 Clear       '}              ║")
        print(f"║  🔥 Gas/Smoke : {'🔴 DETECTED    ' if g else '🟢 Clear       '}              ║")
        print(f"║  🚨 Alarm     : {'🔴 ACTIVE      ' if a else '🟢 Off         '}              ║")
        print("╚══════════════════════════════════════╝")
        print("  Adjust MQ2 pot clockwise until Gas = 🟢 Clear")
        print("  Wave at PIR to test motion detection")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)