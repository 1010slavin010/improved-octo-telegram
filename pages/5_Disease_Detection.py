"""AI crop/plant disease detection page for KisanSense / AgroSentry."""

from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

from utils.auth import require_login
from utils.recommendations import DISEASE_INFO, get_recommendations
from utils.theme import inject_theme, topnav

st.set_page_config(page_title="AI Disease Detection", page_icon="🔬", layout="wide")
require_login()
inject_theme()
topnav("disease")

st.title("🔬 AI Disease Detection")
st.caption(
    "Upload a plant or leaf photo, or use your device camera. "
    "The local trained model analyzes the image without requiring an external AI API."
)

MODEL_CANDIDATES = [
    Path("model/plant_model_v5.keras"),
    Path("model/plant_disease_model.keras"),
    Path("model/plant_disease_model.h5"),
]

# Fallback labels come from the recommendation catalogue shipped with the project.
# If the model stores its own class_names metadata, that metadata is preferred.
FALLBACK_CLASS_NAMES = list(DISEASE_INFO.keys())


def find_model_path() -> Path | None:
    for path in MODEL_CANDIDATES:
        if path.exists():
            return path
    return None


@st.cache_resource(show_spinner=False)
def load_model(model_path: str):
    try:
        import tensorflow as tf

        return tf.keras.models.load_model(model_path)
    except Exception as exc:
        return None, str(exc)


def get_class_names(model):
    # Some exported Keras models carry class names in metadata/config.
    for attr in ("class_names", "classes", "labels"):
        value = getattr(model, attr, None)
        if isinstance(value, (list, tuple)) and value:
            return [str(x) for x in value]

    config = getattr(model, "_config", None)
    if isinstance(config, dict):
        for key in ("class_names", "classes", "labels"):
            value = config.get(key)
            if isinstance(value, (list, tuple)) and value:
                return [str(x) for x in value]

    return FALLBACK_CLASS_NAMES


def predict(image: Image.Image, model, class_names):
    # The trained model expects 224x224 RGB images normalized to 0..1.
    img = image.convert("RGB").resize((224, 224))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    predictions = model.predict(arr, verbose=0)
    preds = np.asarray(predictions).squeeze()

    # Handle models returning a single output tensor or a list containing one.
    if preds.ndim != 1:
        preds = preds.reshape(-1)

    # Convert logits to probabilities if necessary.
    if np.any(preds < 0) or not np.isclose(float(np.sum(preds)), 1.0, atol=0.05):
        exp = np.exp(preds - np.max(preds))
        preds = exp / np.sum(exp)

    top_indices = np.argsort(preds)[::-1][: min(3, len(preds))]
    results = []
    for idx in top_indices:
        idx = int(idx)
        label = class_names[idx] if idx < len(class_names) else f"Class {idx}"
        results.append((label, float(preds[idx])))

    return results


model_path = find_model_path()
model = None
model_error = None

if model_path:
    loaded = load_model(str(model_path))
    if isinstance(loaded, tuple):
        model, model_error = loaded
    else:
        model = loaded
else:
    st.warning(
        "The trained model file is not in this repository yet. Add "
        "`model/plant_model_v5.keras` to enable real disease predictions.",
        icon="⚠️",
    )

if model is None and model_error:
    st.error(f"The disease model could not be loaded: {model_error}")

st.divider()

tab_upload, tab_camera = st.tabs(["📁 Upload photo", "📷 Use camera"])
image_to_predict = None

with tab_upload:
    uploaded = st.file_uploader(
        "Upload a clear photo of the plant or leaf",
        type=["jpg", "jpeg", "png", "webp"],
        help="For best results, keep the affected leaf well lit and mostly inside the frame.",
    )
    if uploaded:
        image_to_predict = Image.open(uploaded)
        st.image(image_to_predict, caption="Uploaded plant/leaf", width=450)

with tab_camera:
    captured = st.camera_input("Take a photo of the plant or leaf")
    if captured:
        image_to_predict = Image.open(captured)
        st.image(image_to_predict, caption="Camera capture", width=450)

if image_to_predict:
    st.info("Tip: photograph one affected leaf closely, with good natural light and minimal background.")

if image_to_predict and st.button("🔍 Detect Disease", type="primary", use_container_width=True):
    if model is None:
        st.error("Disease detection is not ready until `model/plant_model_v5.keras` is added and loads successfully.")
    else:
        with st.spinner("Analyzing leaf image locally..."):
            class_names = get_class_names(model)
            results = predict(image_to_predict, model, class_names)

        best_label, best_confidence = results[0]
        info = get_recommendations(best_label)

        st.subheader("Diagnosis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted condition", info["title"])
        with col2:
            st.metric("Confidence", f"{best_confidence:.1%}")

        if info["is_healthy"]:
            st.success("🌿 The model indicates that the plant appears healthy.")
        elif best_confidence >= 0.70:
            st.warning("⚠️ A possible disease or crop-health issue was detected. Confirm symptoms before treatment.")
        else:
            st.info("ℹ️ Confidence is low. Take another clear close-up photo before acting on the result.")

        st.markdown("### What it may mean")
        st.write(info["description"])

        st.markdown("### Recommended next steps")
        st.write(info["treatment"])

        if len(results) > 1:
            st.markdown("### Other model possibilities")
            for label, confidence in results[1:]:
                st.write(f"• {label.replace('___', ' — ').replace('_', ' ')} — **{confidence:.1%}**")

        st.caption(
            "AI output is a screening aid, not a laboratory diagnosis. If symptoms are severe or spreading rapidly, verify with a local agronomist or agriculture department before applying chemicals."
        )
