# 🌬️ AeroGrid: Hyper-Local Air Quality Intelligence
**Built by Team Vision.exe | Civic Tech & Urban Solutions**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hardware](https://img.shields.io/badge/Hardware-ESP32%20%7C%20LoRa-blue)]()
[![ML](https://img.shields.io/badge/Machine_Learning-Random_Forest-green)]()

## 📌 Project Overview
AeroGrid is a zero-OpEx, hyper-local air quality mesh network. We replace expensive, sparse city-wide monitoring stations with a frugal grid of ESP32-LoRa nodes. By feeding multi-sensor telemetry (PM2.5, Gas, Weather) into a central AI engine, we provide municipal administrators with **ward-level source apportionment** (e.g., separating construction dust from traffic emissions) for targeted civic action.

## ⚙️ The Architecture
1. **The Edge Node:** ESP32 + LoRa SoC integrated with PMS5003 (Particulate), MQ7/MQ135 (Gases), and BME280 (Environment). Powered by 220V grid with 5V supercapacitor backup.
2. **Ward Central Gateway:** Aggregates hex-compressed LoRa packets from 50-100 street nodes, piggybacking on municipal Wi-Fi to eliminate 4G SIM card OpEx.
3. **The Vayu-Niti AI Core:** Enterprise MQTT data ingestion feeding into Scikit-learn Random Forest models to tag pollution sources and trigger automated policy dashboards.

## 📂 Repository Structure
* `/Firmware`: ESP-IDF / C++ code for ESP32 sensor integration and LoRa transmission.
* `/Machine_Learning`: Python scripts and Scikit-learn models for Source Apportionment.
* `/Dashboard`: UI files for the municipal policy and street-level advisory dashboard.

## 🚀 Quick Start (Prototype)
*Hardware Schematics and full deployment instructions are being finalized for the production build.*
