"""AgroSentry shared visual theme."""

import streamlit as st

PAGES = [
    {"key": "home", "label": "Dashboard", "icon": "🏠", "target": "Home.py"},
    {"key": "ai", "label": "AI Assistant", "icon": "🤖", "target": "pages/1_AI_Assistant.py"},
    {"key": "sensor", "label": "Sensors", "icon": "🌡️", "target": "pages/2_Sensor_Dashboard.py"},
    {"key": "alerts", "label": "Alerts", "icon": "🚨", "target": "pages/3_Flood_Drought_Alerts.py"},
    {"key": "camera", "label": "Camera", "icon": "📷", "target": "pages/4_Camera_Feed.py"},
    {"key": "disease", "label": "Disease Scan", "icon": "🔬", "target": "pages/5_Disease_Detection.py"},
]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');
:root{--bg-0:#0a0812;--bg-1:#120f1e;--panel:#161328;--panel-2:#1c1832;--border:rgba(255,255,255,.08);--text-hi:#eef0f7;--text-mid:#b8b7c9;--text-lo:#7d7c94;--accent:#8b5cf6;--accent-2:#6d28d9;--cyan:#22d3ee;--pink:#f43f8d;--amber:#f5b942;--green:#34d399}
html,body,[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse 120% 80% at 20% -10%,#241a3d 0%,var(--bg-0) 45%) fixed;color:var(--text-hi);font-family:'Inter',sans-serif}
[data-testid="stHeader"]{background:transparent}[data-testid="stToolbar"]{right:1rem}
h1,h2,h3,h4,h5{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.01em}h1{font-weight:700!important}p,span,label,div{color:var(--text-mid)}h1,h2,h3,h4,.stMarkdown strong{color:var(--text-hi)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,var(--panel) 0%,var(--bg-1) 100%);border-right:1px solid var(--border)}
.stButton>button,.stDownloadButton>button{border-radius:999px!important;border:1px solid var(--border)!important;background:var(--panel-2)!important;color:var(--text-mid)!important;font-weight:500!important;padding:.45rem 1.1rem!important;transition:all .15s ease}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--accent)!important;color:var(--text-hi)!important}.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--accent) 0%,var(--accent-2) 100%)!important;border:1px solid transparent!important;color:white!important;box-shadow:0 0 18px rgba(139,92,246,.35)}
.fortexa-brand{display:flex;align-items:center;gap:.6rem;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.25rem;color:var(--text-hi);margin-bottom:.2rem}.fortexa-brand .dot{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--cyan),var(--accent));box-shadow:0 0 10px var(--accent)}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker){background:linear-gradient(180deg,var(--panel-2) 0%,var(--panel) 100%);border:1px solid var(--border)!important;border-radius:18px!important;padding:.4rem .2rem}
[data-testid="stMetric"]{background:var(--panel-2);border:1px solid var(--border);border-radius:16px;padding:1rem 1.2rem}[data-testid="stMetricLabel"]{color:var(--text-lo)!important;text-transform:uppercase;font-size:.72rem;letter-spacing:.06em}[data-testid="stMetricValue"]{color:var(--text-hi)!important;font-family:'Space Grotesk',sans-serif}
[data-testid="stAlert"]{border-radius:14px;border:1px solid var(--border);background:var(--panel-2)!important}.stTabs [data-baseweb="tab-list"]{gap:6px}.stTabs [data-baseweb="tab"]{background:var(--panel-2);border-radius:999px;border:1px solid var(--border);padding:6px 18px;color:var(--text-mid)}.stTabs [aria-selected="true"]{background:linear-gradient(135deg,var(--accent) 0%,var(--accent-2) 100%)!important;color:white!important;border-color:transparent!important}
input,textarea,.stTextInput input,.stNumberInput input{background:var(--panel-2)!important;color:var(--text-hi)!important;border-radius:10px!important;border:1px solid var(--border)!important}hr{border-color:var(--border)!important}
.chip{display:inline-flex;align-items:center;gap:6px;padding:3px 12px;border-radius:999px;font-size:.72rem;font-weight:600;letter-spacing:.03em;text-transform:uppercase;border:1px solid var(--border)}.chip-green{background:rgba(52,211,153,.12);color:var(--green);border-color:rgba(52,211,153,.3)}.chip-amber{background:rgba(245,185,66,.12);color:var(--amber);border-color:rgba(245,185,66,.3)}.chip-pink{background:rgba(244,63,141,.12);color:var(--pink);border-color:rgba(244,63,141,.3)}.chip-cyan{background:rgba(34,211,238,.12);color:var(--cyan);border-color:rgba(34,211,238,.3)}
[data-testid="stChatMessage"]{background:var(--panel-2);border:1px solid var(--border);border-radius:16px}
</style>
"""

def inject_theme():
    st.markdown(CSS, unsafe_allow_html=True)

def topnav(active_key: str):
    st.markdown('<div class="fortexa-brand"><span class="dot"></span>AgroSentry — Farm Ops</div>', unsafe_allow_html=True)
    page_registry = st.session_state.get("_pages", {})
    cols = st.columns(len(PAGES))
    for col, page in zip(cols, PAGES):
        with col:
            is_active = page["key"] == active_key
            if st.button(f'{page["icon"]}  {page["label"]}', key=f'nav_{page["key"]}', type="primary" if is_active else "secondary", use_container_width=True):
                if not is_active:
                    destination = page_registry.get(page["key"], page["target"])
                    st.switch_page(destination)
    st.write("")
