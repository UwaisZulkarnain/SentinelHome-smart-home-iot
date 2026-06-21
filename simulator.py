import csv
import os
import random
import math
from datetime import datetime, timedelta

os.makedirs("dataset", exist_ok=True)

# ── Waterfall classifier (mirrors firmware logic) ──────────────────────────
def classify(temp, hum, motion_dur, gas, is_night):
    temp_class = 0
    if temp >= 40: temp_class = 3
    elif temp >= 35: temp_class = 2
    elif temp >= 30: temp_class = 1

    hum_class = 0
    if hum >= 80: hum_class = 2
    elif hum >= 70: hum_class = 1

    motion_class = 0
    if is_night:
        if motion_dur >= 15: motion_class = 3
        elif motion_dur >= 5: motion_class = 2
        elif motion_dur > 0: motion_class = 1
    else:
        if motion_dur >= 60: motion_class = 2
        elif motion_dur >= 30: motion_class = 1

    if gas and is_night and motion_class == 3: return 3, "gas_and_intrusion"
    elif gas and temp >= 35: return 3, "gas_and_hot"
    elif gas: return 3, "gas_only"
    elif temp >= 40: return 3, "extreme_heat"
    elif is_night and motion_class == 3: return 3, "night_intrusion"
    elif temp_class == 2 and hum_class == 2: return 2, "hot_humid"
    elif temp_class == 2: return 2, "hot"
    elif hum_class == 2: return 2, "critical_humidity"
    elif is_night and motion_class == 2: return 2, "night_sustained_motion"
    elif not is_night and motion_class == 2: return 2, "day_unusual_motion"
    elif temp_class == 1 and hum_class == 1: return 1, "warm_humid"
    elif temp_class == 1: return 1, "warm"
    elif hum_class == 1: return 1, "humid"
    elif is_night and motion_class == 1: return 1, "night_brief_motion"
    elif not is_night and motion_class == 1: return 1, "day_lingering_motion"
    else: return 0, "normal"

def gauss(center, std, lo, hi):
    return round(max(lo, min(hi, random.gauss(center, std))), 1)

def gen_row(target_class, is_night, base_time, idx):
    ts = (base_time + timedelta(seconds=idx*2)).isoformat()
    gas = 0
    motion = 0
    motion_dur = 0
    alarm = 0

    # Edge case blend — 10% of rows near boundary
    edge = random.random() < 0.10

    if target_class == 0:
        temp = gauss(26, 1.5, 18, 29.9) if not edge else gauss(29.5, 0.3, 28, 30)
        hum  = gauss(55, 5, 40, 69.9) if not edge else gauss(69, 0.5, 67, 70)
        motion_dur = random.choice([0,0,0,0,1,2]) 
        motion = 1 if motion_dur > 0 else 0

    elif target_class == 1:
        mode = random.choices(['warm','humid','warm_humid','motion'], weights=[3,2,2,3])[0]
        if mode == 'warm':
            temp = gauss(32, 1, 30, 34.9)
            hum  = gauss(55, 5, 40, 69.9)
        elif mode == 'humid':
            temp = gauss(27, 1.5, 18, 29.9)
            hum  = gauss(74, 2, 70, 79.9)
        elif mode == 'warm_humid':
            temp = gauss(32, 1, 30, 34.9)
            hum  = gauss(74, 2, 70, 79.9)
        else:  # motion
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            if is_night:
                motion_dur = random.randint(1, 4)
            else:
                motion_dur = random.randint(1, 29)
            motion = 1
        if edge:
            temp = gauss(30.2, 0.2, 30, 30.8)
            hum  = gauss(70.2, 0.2, 70, 70.8)

    elif target_class == 2:
        mode = random.choices(['hot','critical_hum','hot_humid','night_motion','day_motion'], weights=[2,2,2,2,2])[0]
        if mode == 'hot':
            temp = gauss(37, 1, 35, 39.9)
            hum  = gauss(55, 5, 40, 69.9)
        elif mode == 'critical_hum':
            temp = gauss(27, 1.5, 18, 29.9)
            hum  = gauss(83, 2, 80, 89.9)
        elif mode == 'hot_humid':
            temp = gauss(37, 1, 35, 39.9)
            hum  = gauss(83, 2, 80, 89.9)
        elif mode == 'night_motion':
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            motion_dur = random.randint(5, 14)
            motion = 1
        else:  # day_motion
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            motion_dur = random.randint(60, 119)
            motion = 1
        if edge:
            temp = gauss(35.2, 0.2, 35, 35.8)

    elif target_class == 3:
        mode = random.choices(['gas','extreme_heat','night_intrusion','gas_hot','gas_intrusion'], weights=[3,2,2,2,1])[0]
        if mode == 'gas':
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            gas = 1
        elif mode == 'extreme_heat':
            temp = gauss(42, 1.5, 40, 50)
            hum  = gauss(55, 5, 40, 69.9)
        elif mode == 'night_intrusion':
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            motion_dur = random.randint(15, 60)
            motion = 1
        elif mode == 'gas_hot':
            temp = gauss(37, 1, 35, 45)
            hum  = gauss(55, 5, 40, 69.9)
            gas = 1
        else:  # gas_intrusion
            temp = gauss(26, 1.5, 18, 29.9)
            hum  = gauss(55, 5, 40, 69.9)
            gas = 1
            motion_dur = random.randint(15, 60)
            motion = 1
        if edge:
            temp = gauss(40.2, 0.2, 40, 40.8)

    cls, reason = classify(temp, hum, motion_dur, gas, is_night)
    alarm = 1 if cls >= 2 else 0

    return ts, temp, hum, motion, gas, alarm, is_night, motion_dur, cls, reason

# ── Main ───────────────────────────────────────────────────────────────────
print("SentinelHome Synthetic Data Generator")
print("=" * 45)
print("Classes: 0=Normal  1=Comfort Alert  2=Warning  3=Danger")
print()

target_class = int(input("Select class (0/1/2/3): ").strip())
is_night_input = input("Day or Night? (d/n): ").strip().lower()
is_night = is_night_input == 'n'
n_rows = int(input("How many rows? (recommended 3000): ").strip())

time_label = "night" if is_night else "day"
base_time = datetime.now().replace(
    hour=23 if is_night else 10,
    minute=0, second=0, microsecond=0
)

raw_file = f"dataset/sensor_class{target_class}_{time_label}_raw.csv"
proc_file = f"dataset/sensor_class{target_class}_{time_label}_processed.csv"

raw_cols = ["created_at","temperature","humidity","motion","gas","is_night","motion_duration_sec"]
proc_cols = ["created_at","temperature","humidity","motion","gas","alarm","is_night","motion_duration_sec","class","reason"]

with open(raw_file, "w", newline="") as rf, open(proc_file, "w", newline="") as pf:
    rw = csv.writer(rf)
    pw = csv.writer(pf)
    rw.writerow(raw_cols)
    pw.writerow(proc_cols)

    actual_class_counts = {}
    for i in range(n_rows):
        ts, t, h, m, g, a, n, dur, cls, reason = gen_row(target_class, is_night, base_time, i)
        rw.writerow([ts, t, h, m, g, n, dur])
        pw.writerow([ts, t, h, m, g, a, n, dur, cls, reason])
        actual_class_counts[cls] = actual_class_counts.get(cls, 0) + 1
        if (i+1) % 500 == 0:
            print(f"  {i+1}/{n_rows} rows generated...")

print(f"\nDone! {n_rows} rows saved.")
print(f"  Raw:       {raw_file}")
print(f"  Processed: {proc_file}")
print(f"\nActual class distribution:")
for c in sorted(actual_class_counts):
    print(f"  Class {c}: {actual_class_counts[c]} rows ({actual_class_counts[c]/n_rows*100:.1f}%)")