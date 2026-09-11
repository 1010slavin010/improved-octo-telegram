# KisanSense — Smart Farming Assistant

A Streamlit-based SIH prototype for farmer-friendly crop monitoring and decision support.

## Current prototype

- 🌾 Farm operations home screen
- 🌡️ Soil moisture, temperature, humidity and light telemetry
- 🤖 Local sensor-based AI Assistant — no external LLM API required
- 🔬 Plant/leaf disease screening using `model/plant_model_v5.keras`
- 📷 Camera input and image upload in Disease Detection
- 🐛 Sensor-driven pest-risk guidance
- 🚨 Flood/drought risk alerts
- 📊 Sensor history and telemetry dashboard
- 🔐 Optional password protection through Streamlit secrets
- 📱 Streamlit layout suitable for desktop and mobile browsers

## Run locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run Home.py
```

If `streamlit` is already on PATH, this also works:

```bash
streamlit run Home.py
```

## Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and set `APP_PASSWORD` if password protection is enabled.

Never commit the real `secrets.toml` file.

## Disease model

The repository contains `model/plant_model_v5.keras`. The Disease Detection page looks for this model first and falls back to compatible model filenames if present.

The model is used as a screening aid; field confirmation is recommended before treatment decisions.

## Hardware / future deployment

The ESP32 firmware is included for the hardware prototype. The Streamlit app can run with demo telemetry until a compatible sensor endpoint is configured. LoRa, Raspberry Pi edge deployment and additional field hardware are future deployment stages, not claims that the cloud prototype is already connected to them.

## Project structure

```text
Home.py
pages/
  1_AI_Assistant.py
  2_Sensor_Dashboard.py
  3_Flood_Drought_Alerts.py
  4_Camera_Feed.py
  5_Disease_Detection.py
  6_Pest_Control.py
utils/
  ai_agent.py
  auth.py
  esp_client.py
  pest_advisor.py
  recommendations.py
  theme.py
model/
  plant_model_v5.keras
esp32_firmware/
  esp32_firmware.ino
requirements.txt
runtime.txt
```

## Streamlit deployment

Use `Home.py` as the main file when deploying to Streamlit Community Cloud or another Streamlit host.
