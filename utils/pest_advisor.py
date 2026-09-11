"""AgroSentry pest-risk scoring and sticky-trap counting."""
import numpy as np
from PIL import Image

def _rule_aphids(temp, hum, soil):
    if temp >= 22 and hum <= 55:
        level = "HIGH" if temp >= 27 and hum <= 45 else "MODERATE"
        return {"pest":"Aphids","risk_level":level,"reason":f"Warm, dry conditions ({temp}°C, {hum}% humidity) favor rapid aphid reproduction.","organic_treatment":"Introduce ladybugs/lacewings, or spray neem oil (1-2 tbsp/gallon water + a drop of mild soap) in late afternoon.","chemical_treatment":"Insecticidal soap or pyrethrin spray if infestation is severe."}
    return None

def _rule_spider_mites(temp, hum, soil):
    if temp >= 25 and hum <= 50:
        level = "HIGH" if temp >= 30 and hum <= 35 else "MODERATE"
        return {"pest":"Spider mites","risk_level":level,"reason":f"Hot, dry air ({temp}°C, {hum}% humidity) is prime spider-mite weather.","organic_treatment":"Increase leaf humidity with a light overhead misting; spray diluted neem oil on leaf undersides.","chemical_treatment":"Miticide (e.g. abamectin) if webbing is already visible."}
    return None

def _rule_fungus_gnats(temp, hum, soil):
    if soil >= 65 and hum >= 60:
        level = "HIGH" if soil >= 80 else "MODERATE"
        return {"pest":"Fungus gnats","risk_level":level,"reason":f"Waterlogged soil ({soil}%) and high humidity ({hum}%) let larvae thrive in the topsoil.","organic_treatment":"Let the top inch of soil dry between waterings; apply yellow sticky traps near the base of plants.","chemical_treatment":"Bti (Bacillus thuringiensis israelensis) soil drench."}
    return None

def _rule_whiteflies(temp, hum, soil):
    if temp >= 21 and 40 <= hum <= 70:
        return {"pest":"Whiteflies","risk_level":"MODERATE","reason":f"Mild, humid conditions ({temp}°C, {hum}% humidity) suit whitefly breeding cycles.","organic_treatment":"Yellow sticky traps, reflective mulch, or a strong water spray on leaf undersides.","chemical_treatment":"Insecticidal soap or neem oil applied every 5-7 days until under control."}
    return None

_RISK_RULES = [_rule_aphids, _rule_spider_mites, _rule_fungus_gnats, _rule_whiteflies]
_LEVEL_RANK = {"NORMAL":0,"MODERATE":1,"HIGH":2}

def compute_pest_risks(sensor_data: dict) -> dict:
    temp = float(sensor_data.get("temperature", 24.0))
    hum = float(sensor_data.get("humidity", 55.0))
    soil = float(sensor_data.get("soil_moisture", 45.0))
    risks = []
    for rule in _RISK_RULES:
        result = rule(temp, hum, soil)
        if result:
            risks.append(result)
    overall = "NORMAL" if not risks else max((r["risk_level"] for r in risks), key=lambda lvl: _LEVEL_RANK[lvl])
    return {"overall_level":overall,"risks":risks}

def count_trap_pests(image: Image.Image) -> dict:
    img = image.convert("RGB").resize((300, 300))
    arr = np.asarray(img, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_yellowish = (r > 140) & (g > 120) & (b < 150) & (np.abs(r - g) < 60)
    brightness = (r + g + b) / 3.0
    is_dark = brightness < 110
    pest_mask = is_dark & (~is_yellowish)
    visited = np.zeros_like(pest_mask, dtype=bool)
    h, w = pest_mask.shape
    blob_count = 0
    for y in range(h):
        for x in range(w):
            if pest_mask[y, x] and not visited[y, x]:
                stack = [(y, x)]
                visited[y, x] = True
                size = 0
                while stack:
                    cy, cx = stack.pop()
                    size += 1
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and pest_mask[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            stack.append((ny, nx))
                if size >= 6:
                    blob_count += 1
    if blob_count == 0: density = "CLEAN"
    elif blob_count <= 8: density = "LOW"
    elif blob_count <= 25: density = "MODERATE"
    else: density = "HIGH"
    advice = {"CLEAN":"No pests detected on the trap. Keep monitoring weekly.","LOW":"Light pest presence. Keep the trap up and recheck in a few days.","MODERATE":"Noticeable pest pressure. Consider organic treatment (neem oil, beneficial insects) this week.","HIGH":"High pest load. Treat promptly and consider adding more traps around the field to isolate the hotspot."}[density]
    return {"pest_count":blob_count,"density":density,"advice":advice}
