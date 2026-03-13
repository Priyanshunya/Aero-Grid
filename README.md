# 🏙️ AeroGrid: Hyper-Local Air Quality Intelligence
**Built by Team Vision.exe**

AeroGrid is a zero-OpEx, hyper-local air quality mesh network. We replace expensive, sparse city-wide monitoring stations with a frugal grid of ESP32-LoRa nodes. By feeding multi-sensor telemetry into a central AI engine, we provide municipal administrators with **ward-level source apportionment** (e.g., separating construction dust from traffic emissions) for targeted civic action.

---

## ⚙️ The Architecture
1. **The Edge Node:** ESP32 + LoRa SoC integrated with PMS5003 (Particulate), MQ7/MQ135 (Gases), and BME280 (Environment). Powered by a 220V grid-tie with a 5V supercapacitor backup.
2. **Ward Central Gateway:** Aggregates hex-compressed LoRa packets from 50-100 street nodes, piggybacking on municipal Wi-Fi to eliminate 4G SIM card OpEx.
3. **The AI Core:** Enterprise MQTT data ingestion feeding into Scikit-Learn Random Forest models to tag pollution sources and trigger automated policy dashboards.

## 🛠️ Hardware Bill of Materials (BoM)
* **Microcontroller:** ESP32 with integrated LoRa transceiver
* **Particulate Sensor:** PMS5003 (Optical PM1.0, PM2.5, PM10)
* **Gas Sensors:** MQ-135 (VOCs/Smoke) and MQ-7 (Carbon Monoxide)
* **Environmental Sensor:** BME280 (Temperature, Humidity, Pressure)
* **Power Infrastructure:** 220V AC Grid-Tie module + 5V Supercapacitor

## 🎯 Design Rationale: Why This Specific Stack?
We engineered this hardware array to avoid the bloated costs of traditional lab-grade reference stations. Every component was chosen to feed high-value proxy signals to our AI model:

* **Hardware as Feature Engineering:** We didn't choose random sensors; we chose specific *chemical proxies*. The **MQ-7** isolates traffic emissions (CO), the **PMS5003** isolates construction dust (heavy PM), and the **MQ-135** captures biomass burning (generic VOCs/smoke). This minimal array gives our Random Forest model exactly the distinct signatures it needs for accurate source apportionment.
* **Environmental Calibration:** Cheap gas sensors are notoriously noisy due to weather changes. We strictly included the **BME280** to provide a baseline to mathematically calibrate and smooth the MQ sensor data against temperature and humidity fluctuations before it hits the AI pipeline.
* **Zero-OpEx Connectivity & Power:** By utilizing the **ESP32's LoRa mesh** capabilities, we eliminated recurring cellular data costs. By using a **Grid-Tie + Supercapacitor** instead of solar panels and lithium batteries, we eliminated the two biggest points of failure in urban IoT: dust-covered solar arrays and dead batteries. 

## 📂 Repository Structure (Prototype Logic)
This repository contains the Proof of Concept (PoC) architectural logic and codebase structures developed during the hackathon:

* `/Hardware_Node` : C++ structural logic for ESP32 sensor integration, environmental calibration, and LoRa mesh transmission.
* `/Machine_Learning` : Python framework outlining our feature engineering and Random Forest classification pipeline.
* `/Dashboard` : UI layout and data visualization framework for the municipal policy dashboard.

## 🚀 Project Status
AeroGrid is currently in the **Phase 1 Proof-of-Concept** stage for the India Innovates 2026 evaluation. 

The files in this repository demonstrate the system's structural logic, sensor data handling, and AI inference pipeline. Full production deployment binaries, live dataset links, and local compiling instructions will be released upon moving to the hardware deployment phase. 

---
*Built for the India Innovates 2026 Hackathon.*
