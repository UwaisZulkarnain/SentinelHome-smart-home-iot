# Khamsah — ML Dataset Guide

## Setup
pip install requests scikit-learn pandas matplotlib

## Collect Dataset
python tools/collect_dataset.py

Choose:
- Option 1 = normal data (baseline)
- Option 2 = anomaly data (triggered events)
- Option 3 = full dataset

Files saved to dataset/ folder.

## Anomaly Scenarios to Capture
Ask Uwais to do these while XIAO is running:
1. Wave hand repeatedly at PIR (motion anomaly)
2. Blow near MQ-2 sensor (gas anomaly)
3. Cover DHT11 with hand (temp/humidity spike)
4. Leave idle 30 mins (normal baseline)

## Suggested ML Approach
- Algorithm: Isolation Forest (sklearn)
- Train on: normal data only
- Test on: anomaly data
- Features: temperature, humidity, motion, gas, alarm

## Quick Start ML Script
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load data
normal = pd.read_csv("dataset/sensor_normal_XXXXXX.csv")
anomaly = pd.read_csv("dataset/sensor_anomaly_XXXXXX.csv")

features = ["temperature", "humidity", "motion", "gas", "alarm"]
X_train = normal[features].dropna()
X_test = anomaly[features].dropna()

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train_scaled)

preds = model.predict(X_test_scaled)
anomaly_count = (preds == -1).sum()
print(f"Anomalies detected: {anomaly_count}/{len(preds)}")