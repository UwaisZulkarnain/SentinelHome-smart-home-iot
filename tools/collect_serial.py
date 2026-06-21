import serial
import csv
import os
import time
from datetime import datetime

PORT = "COM10"
BAUD = 115200

os.makedirs("dataset", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_file = f"dataset/sensor_raw_{timestamp}.csv"
processed_file = f"dataset/sensor_processed_{timestamp}.csv"

print(f"Connecting to {PORT}...")
ser = serial.Serial(PORT, BAUD, timeout=2)
time.sleep(2)

raw_f = open(raw_file, "w", newline="")
proc_f = open(processed_file, "w", newline="")
raw_writer = csv.writer(raw_f)
proc_writer = csv.writer(proc_f)

raw_writer.writerow(["created_at","temperature","humidity","motion","gas","is_night","motion_duration_sec"])
proc_writer.writerow(["created_at","temperature","humidity","motion","gas","alarm","is_night","motion_duration_sec","class","reason"])

print(f"Logging to:\n  {raw_file}\n  {processed_file}")
print("Ctrl+C to stop\n")

count = 0
try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line.startswith("T:"):
            continue
        try:
            # Replace longer patterns first to avoid substring issues (e.g. REASON: contains A:)
            parts = line.replace("T:","").replace("REASON:","|").replace("CLASS:","|").replace("DUR:","|").replace("H:","|").replace("M:","|").replace("G:","|").replace("A:","|").replace("N:","|").split("|")
            t = float(parts[0])
            h = float(parts[1])
            m = int(parts[2])
            g = int(parts[3])
            a = int(parts[4])
            n = int(parts[5])
            dur = int(parts[6])
            cls = int(parts[7])
            reason = parts[8].strip()
            ts = datetime.now().isoformat()

            raw_writer.writerow([ts, t, h, m, g, n, dur])
            proc_writer.writerow([ts, t, h, m, g, a, n, dur, cls, reason])
            raw_f.flush()
            proc_f.flush()
            count += 1
            print(f"[{count}] T:{t} H:{h} M:{m} G:{g} N:{n} DUR:{dur} CLASS:{cls} {reason}")
        except Exception as e:
            print(f"Parse error: {e} | line: {line}")
except KeyboardInterrupt:
    print(f"\nStopped. {count} rows saved.")
    raw_f.close()
    proc_f.close()