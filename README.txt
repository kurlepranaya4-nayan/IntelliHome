# IoT Smart Home Automation Dashboard

A beginner-friendly, runnable college project prototype. It simulates smart devices and sensors and provides an interactive dashboard.

## Run on Windows

1. Install Python 3.10 or newer from https://www.python.org/downloads/ (tick **Add Python to PATH** during installation).
2. Extract this ZIP folder.
3. Open the extracted folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run these commands:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If `py` does not work, try replacing `py` with `python`.

The dashboard should open in your browser. If it does not, open the local address shown in the terminal (usually http://localhost:8501).

## Run on Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Features
- Switch simulated bedroom/living room lights, fan, and air conditioner on/off.
- Display simulated temperature and humidity.
- Refresh sensor values.
- Apply a simple energy-saving automation rule.
- Estimate power use, energy use, and example electricity cost.
- View a live chart of estimated device power.

## Important limitations
This version is a software simulation. It does **not** connect to real devices or use MQTT, Firebase, or ESP32 hardware yet. Energy values and the ₹8/kWh rate are illustrative. If presenting it, describe it as a simulated prototype and explain how MQTT/ESP32 integration could be added in a future version.

## Viva introduction
"My project is an IoT Smart Home Automation Dashboard. It provides a single interface to control simulated home appliances, monitor temperature and humidity, and estimate energy consumption. Python handles the application logic, while Streamlit provides the web interface and Plotly displays the energy chart. At this stage, devices and sensors are simulated. The future scope is to connect ESP32 hardware through MQTT and store sensor history in a database."
