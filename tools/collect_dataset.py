import requests
import csv
import os
from datetime import datetime

SUPABASE_URL = "https://ubcyktzfiylqirzpdqnu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InViY3lrdHpmaXlscWlyenBkcW51Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE4MDkxNjQsImV4cCI6MjA5NzM4NTE2NH0.Gu0jBFdVnsBMFF2VWliTnoKtBqCt_-IwSQfnoe2ts9c"

print("SentinelHome Dataset Collector")
print("=" * 40)
print("1. Normal data (baseline - no events)")
print("2. Anomaly data (trigger sensors during collection)")
print("3. Full dataset (everything)")
choice = input("Select (1/2/3): ").strip()

label_map = {"1": "normal", "2": "anomaly", "3": "full"}
label = label_map.get(choice, "full")

r = requests.get(
    f"{SUPABASE_URL}/rest/v1/sensor_readings?select=*&order=created_at.asc&limit=10000",
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
)

rows = r.json()

# Filter based on choice
if label == "normal":
    rows = [r for r in rows if not r.get("motion") and not r.get("gas") and not r.get("alarm")]
    print(f"Filtered to {len(rows)} normal rows (no motion/gas/alarm)")
elif label == "anomaly":
    rows = [r for r in rows if r.get("motion") or r.get("gas") or r.get("alarm")]
    print(f"Filtered to {len(rows)} anomaly rows (motion/gas/alarm events)")
else:
    print(f"Full dataset: {len(rows)} rows")

os.makedirs("dataset", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"dataset/sensor_{label}_{timestamp}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["created_at","temperature","humidity","motion","gas","alarm"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved to {filename}")
print(f"Total rows: {len(rows)}")