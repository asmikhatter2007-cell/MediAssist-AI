import streamlit as st
import requests
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar(3)

BASE_URL = "http://127.0.0.1:8000"

# CHANGE THIS before submission / demo - different from Admin's password
STAFF_PASSWORD = "staff123"

# Theme Styles Injector
st.markdown("""
<style>
header[data-testid="stHeader"]{ background: #0C1024 !important; }
html, body{ background: #0C1024 !important; }
.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

.title-container { display: flex; align-items: center; gap: 15px; margin-bottom: 5px; }
.title-icon { font-size: 2.8rem; }
.title-text {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
}

h2, h3 { color:#EDEFFC !important; font-weight:700 !important; }
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:20px !important;
}
.status-pill { padding: 10px 20px; border-radius: 12px; font-weight: 700; display: inline-block; margin-bottom: 15px; }
.status-functional { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
.status-busy { background: rgba(251,191,110,0.15); color: #FBBF6E; border: 1px solid rgba(251,191,110,0.3); }
.status-overwhelmed { background: rgba(248,113,113,0.15); color: #F87171; border: 1px solid rgba(248,113,113,0.3); }
.metric-header { font-size: 14.5px; font-weight: 600; color: #9BA3C7; margin-bottom: 2px; }
.metric-value { font-size: 34px; font-weight: 800; color: #2DD4BF; margin-top: 0px; }
.stButton>button{
    width:100%; border-radius:16px; height:52px;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%);
    background-size: 200% auto; color:#0C1024; font-size:17px; font-weight:800; border:none;
}
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <span class="title-icon">📊</span>
    <span class="title-text">Emergency Department Dashboard</span>
</div>
""", unsafe_allow_html=True)
st.caption("Real-Time Hospital Resource Analytics")

# ---------------- LOGIN GATE ----------------
if "staff_authenticated" not in st.session_state:
    st.session_state.staff_authenticated = False

if not st.session_state.staff_authenticated:
    with st.container(border=True):
        st.subheader("🔑 Staff Login")
        password_input = st.text_input("Password", type="password")
        if st.button("Login"):
            if password_input == STAFF_PASSWORD:
                st.session_state.staff_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    st.stop()

col_a, col_b = st.columns([5, 1])
with col_a:
    st.success("Logged in as Staff")
with col_b:
    if st.button("Logout"):
        st.session_state.staff_authenticated = False
        st.rerun()

# ---------------- FETCH REAL DATA FROM BACKEND ----------------
try:
    response = requests.get(f"{BASE_URL}/admin/hospital_data")
    response.raise_for_status()
    data = response.json()
except Exception:
    data = None
    st.error("Backend is not running.")

if data is not None and not data.get("has_data"):
    st.warning("No hospital data has been submitted by admin yet.")
elif data is not None:
    admin_data = data["admin_data"]
    status = data["predicted_status"]
    status_message = data["predicted_status_message"]

    status_class = {
        "Functional": "status-functional",
        "Overcrowded": "status-busy",
        "Overwhelmed": "status-overwhelmed",
    }.get(status, "status-busy")

    status_icon = {"Functional": "🟢", "Overcrowded": "🟠", "Overwhelmed": "🔴"}.get(status, "🟠")

    st.markdown(
        f'<div class="status-pill {status_class}">{status_icon} System Status: {status}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Last Updated: {admin_data['last_updated']}")
    st.caption(status_message)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-header">🧑‍🤝‍🧑 Patients in ED</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["current_patients_ed"]}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-header">🛏️ Beds Available</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["beds_available"]}</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-header">🚪 Boarding in ED</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["patients_boarding_ed"]}</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-header">⏱️ Avg Boarding Hrs</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["avg_boarding_hours"]}</div>', unsafe_allow_html=True)

    st.write("")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown('<div class="metric-header">🩺 Total Doctors</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["total_doctors"]}</div>', unsafe_allow_html=True)
    with c6:
        st.markdown('<div class="metric-header">👩‍⚕️ Total Nurses</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["total_nurses"]}</div>', unsafe_allow_html=True)
    with c7:
        st.markdown('<div class="metric-header">🧪 Pending Labs</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["pending_lab_orders"]}</div>', unsafe_allow_html=True)
    with c8:
        st.markdown('<div class="metric-header">🩻 Pending Imaging</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{admin_data["pending_imaging_orders"]}</div>', unsafe_allow_html=True)