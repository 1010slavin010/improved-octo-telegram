"""Connects AgroSentry to an ESP32/Raspberry Pi gateway."""

import time
import random
from io import BytesIO
import requests
import streamlit as st

DEFAULT_ESP_BASE_URL = "http://192.168.31.57"
DATA_ENDPOINT = "/data"
CAMERA_ENDPOINT = "/capture"
TIMEOUT_SECONDS = 3

_global_esp_url = DEFAULT_ESP_BASE_URL
_last_push_data = None
_last_push_time = 0


def set_base_url(url: str):
    global _global_esp_url
    _global_esp_url = url.strip().rstrip("/")
    try:
        if "esp_base_url" in st.session_state:
            st.session_state["esp_base_url"] = _global_esp_url
    except Exception:
        pass


def get_device_base_url() -> str:
    try:
        if "esp_base_url" in st.session_state and st.session_state.get("esp_base_url"):
            return st.session_state.get("esp_base_url", "").strip().rstrip("/")
    except Exception:
        pass
    return _global_esp_url


def record_push_data(payload: dict) -> dict:
    global _last_push_data, _last_push_time
    soil = payload.get("soil_moisture") or payload.get("soil") or payload.get("moisture")
    if soil is not None:
        try:
            soil = float(soil)
            if soil > 100:
                soil = round(max(0.0, min(100.0, (1.0 - (soil - 1000) / 2500) * 100)), 1)
        except Exception:
            soil = 45.0
    else:
        soil = 48.0

    light = payload.get("light_lux") or payload.get("light") or payload.get("lux") or payload.get("ldr")
    if light is not None:
        try:
            light = float(light)
            if light < 4096 and "lux" not in str(payload).lower():
                light = round(max(100.0, min(80000.0, (light / 4095.0) * 65000.0)), 0)
        except Exception:
            light = 42000.0
    else:
        light = 42000.0

    temp = payload.get("temperature") or payload.get("temp") or 25.4
    hum = payload.get("humidity") or payload.get("hum") or 62.0

    _last_push_data = {
        "soil_moisture": round(float(soil), 1),
        "light_lux": round(float(light), 0),
        "temperature": round(float(temp), 1),
        "humidity": round(float(hum), 1),
        "timestamp": time.strftime("%H:%M:%S"),
        "source": "ESP32 (192.168.31.57)",
    }
    _last_push_time = time.time()
    return _last_push_data


def _demo_sensor_reading() -> dict:
    return {
        "soil_moisture": round(random.uniform(42, 60), 1),
        "light_lux": round(random.uniform(38000, 56000), 0),
        "temperature": round(random.uniform(23, 28), 1),
        "humidity": round(random.uniform(55, 75), 1),
        "timestamp": time.strftime("%H:%M:%S"),
        "source": "demo (waiting for ESP32)",
    }


def get_sensor_data() -> dict:
    global _last_push_data, _last_push_time
    if _last_push_data and time.time() - _last_push_time < 15:
        return _last_push_data

    base_url = get_device_base_url()
    if base_url:
        try:
            resp = requests.get(f"{base_url}{DATA_ENDPOINT}", timeout=TIMEOUT_SECONDS)
            if resp.status_code == 200:
                return record_push_data(resp.json())
        except Exception:
            pass

    return _demo_sensor_reading()


def get_camera_snapshot():
    base_url = get_device_base_url()
    if not base_url:
        return None
    try:
        resp = requests.get(f"{base_url}{CAMERA_ENDPOINT}", timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            return BytesIO(resp.content)
    except Exception:
        pass
    return None
