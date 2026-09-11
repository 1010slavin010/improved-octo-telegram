import streamlit as st
from PIL import Image
from utils.esp_client import get_sensor_data
from utils.pest_advisor import compute_pest_risks, count_trap_pests

st.title("🐛 Pest Control")
st.caption("Environmental pest-risk forecasting plus optional sticky-trap photo counting — no extra hardware or trained model required.")
try:
    from utils.theme import inject_theme
    inject_theme()
except Exception:
    pass
st.divider()

st.subheader("🌡️ Environmental Pest Risk")
st.write("Based on your current temperature, humidity, and soil moisture readings — the same conditions that drive your flood/drought alerts.")
sensor_data = get_sensor_data()
result = compute_pest_risks(sensor_data)
level_colors = {"NORMAL": "🟢", "MODERATE": "🟡", "HIGH": "🔴"}
st.markdown(f"### Overall risk: {level_colors.get(result['overall_level'], '⚪')} {result['overall_level']}")
if not result["risks"]:
    st.success("No elevated pest risk under current conditions. Keep monitoring.")
else:
    for risk in result["risks"]:
        with st.container(border=True):
            st.markdown(f"**{level_colors.get(risk['risk_level'], '⚪')} {risk['pest']} — {risk['risk_level']} risk**")
            st.write(risk["reason"])
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("🌿 **Organic option**")
                st.write(risk["organic_treatment"])
            with col2:
                st.markdown("🧪 **If needed**")
                st.write(risk["chemical_treatment"])

st.divider()
st.subheader("📷 Sticky Trap Counter")
st.write("Photograph a yellow sticky trap from the field, and this will estimate pest population from the count of insects caught on it.")
trap_photo = st.file_uploader("Upload a sticky trap photo", type=["jpg", "jpeg", "png"])
use_camera = st.checkbox("Use camera instead")
camera_photo = st.camera_input("Take a photo of the trap") if use_camera else None
photo_file = camera_photo or trap_photo
if photo_file is not None:
    image = Image.open(photo_file)
    st.image(image, caption="Trap photo", width=350)
    with st.spinner("Counting..."):
        trap_result = count_trap_pests(image)
    density_colors = {"CLEAN": "🟢", "LOW": "🟢", "MODERATE": "🟡", "HIGH": "🔴"}
    st.markdown(f"### {density_colors.get(trap_result['density'], '⚪')} {trap_result['pest_count']} insects detected — {trap_result['density']} density")
    st.info(trap_result["advice"])
else:
    st.caption("No photo yet — upload one or switch on the camera above.")
