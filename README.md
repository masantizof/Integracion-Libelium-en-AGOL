# 📡 IoT Environmental Sensor Network Analysis

![Python](https://img.shields.io/badge/Python-Jupyter-orange) ![IoT](https://img.shields.io/badge/Hardware-Libelium-lightgrey) ![Data](https://img.shields.io/badge/Data-Real--Time-red)

## 📋 Project Overview
This notebook documents the data engineering pipeline for a real-time environmental monitoring network deployed in **Puerto Salgar**. It interfaces with **Libelium IoT gateways** to extract, clean, and visualize high-frequency micro-climatic data (Temperature, Humidity, Pressure).

## 🔍 Key Features
* **API Integration:** Connects to the device cloud to fetch JSON payloads containing telemetry data.
* **Quality Control (QA/QC):** Algorithmic detection of sensor anomalies, gaps in transmission, and outliers before data analysis.
* **Interactive Visualization:** Uses `plotly` to render interactive time-series charts, allowing stakeholders to zoom in on specific weather events.

## 🛠️ Tech Stack
* **Environment:** Jupyter Notebook.
* **Libraries:** `pandas` (Time-series manipulation), `requests` (API), `plotly` (Dashboards), `json`.
* **Hardware Context:** Smart Agriculture & Environmental Sensors.

## 💡 Professional Relevance
Demonstrates the ability to handle the full data lifecycle—from hardware sensors in the field to actionable insights on a screen.
