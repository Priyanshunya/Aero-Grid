# Vayu-Niti AI Core: Source Apportionment Inference Pipeline
# Uses Scikit-Learn Random Forest to classify multi-sensor telemetry streams.
# TODO: Move from PySerial to MQTT ingestion for Phase 2 ESP32 Mesh

import pandas as pd
import numpy as np
import serial
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings

# Suppress sklearn feature name warnings for clean console output
warnings.filterwarnings('ignore') 

# --- 1. ML Pipeline & Model Setup ---
print("[AI Core] Initializing Vayu-Niti Source Apportionment Model...")

# Define feature columns matching our sensor payload
FEATURE_NAMES = ['CO_Level', 'VOC_Level', 'PM_Density']
CLASS_MAP = {
    0: "Urban Smog (Delhi Baseline)",
    1: "Traffic Emissions Hotspot",
    2: "⚠️ BIOMASS/WASTE BURNING DETECTED",
    3: "Construction Dust"
}

# Initialize Random Forest with balanced class weights
rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, class_weight='balanced', random_state=42)
scaler = StandardScaler()

# Synthetic calibration baseline for the PoC 
# Simulating standard AQI bounds vs. anomaly spikes (e.g., burning paper demo)
X_calib = pd.DataFrame([
    [150, 120, 0.05], [160, 130, 0.08], # Class 0: Urban Smog (Delhi)
    [300, 250, 0.30], [310, 260, 0.35], # Class 1: Traffic (High CO)
    [180, 420, 0.70], [190, 450, 0.85], # Class 2: Biomass (Huge VOC/PM spike)
    [140, 130, 0.60], [150, 140, 0.65]  # Class 3: Construction (High PM only)
], columns=FEATURE_NAMES)
y_calib = np.array([0, 0, 1, 1, 2, 2, 3, 3])

# Fit the preprocessing scaler and train the model
X_scaled = scaler.fit_transform(X_calib)
rf_model.fit(X_scaled, y_calib)

print(f"[AI Core] Model trained successfully.")
print(f"[AI Core] Feature Importances: CO: {rf_model.feature_importances_[0]:.2f}, VOC: {rf_model.feature_importances_[1]:.2f}, PM: {rf_model.feature_importances_[2]:.2f}")

# --- 2. Live Telemetry Ingestion ---
SERIAL_PORT = 'COM3' # Update based on OS (e.g., /dev/ttyUSB0)
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"[Gateway] Listening for Edge Node on {SERIAL_PORT}...")
    time.sleep(2) 
except Exception as e:
    print(f"[Error] Serial connection failed: {e}")
    print("[System] Waiting for hardware to come online...")

print("\n--- 🟢 VAYU-NITI LIVE AI FEED ACTIVE ---")

while True:
    try:
        if 'ser' in locals() and ser.is_open and ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            # Parse incoming string: TEMP:xx|HUM:xx|MQ7:xx|MQ135:xx|PM:xx
            if "MQ7:" in line and "PM:" in line:
                parts = line.split('|')
                
                # Extract raw sensor values
                mq7_raw = float(parts[2].split(':')[1])
                mq135_raw = float(parts[3].split(':')[1])
                pm_raw = float(parts[4].split(':')[1])
                
                # 1. Format data for the ML Pipeline
                live_features = pd.DataFrame([[mq7_raw, mq135_raw, pm_raw]], columns=FEATURE_NAMES)
                
                # 2. Preprocess (Scale features based on training baseline)
                live_scaled = scaler.transform(live_features)
                
                # 3. AI Inference & Confidence Score
                prediction = rf_model.predict(live_scaled)[0]
                probabilities = rf_model.predict_proba(live_scaled)[0]
                confidence = max(probabilities) * 100
                
                # 4. Actionable Output mapping
                detected_source = CLASS_MAP.get(prediction, "Unknown Anomaly")
                
                print(f"Telemetry -> CO: {mq7_raw:.0f} | VOC: {mq135_raw:.0f} | PM: {pm_raw:.2f}")
                print(f"🤖 AI Inference -> {detected_source} (Confidence: {confidence:.1f}%)\n")
                
    except KeyboardInterrupt:
        print("\n[System] Shutting down AI Core...")
        break
    except Exception:
        # Drop malformed serial packets silently
        pass
