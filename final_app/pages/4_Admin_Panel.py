import streamlit as st
import requests
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Admin", page_icon="🔐", layout="wide")
render_sidebar(4)

BASE_URL = "https://mediassist-ai-68lg.onrender.com"

# CHANGE THIS before submission / demo
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

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
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 800 !important; font-size: 2.5rem !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:20px !important;
}
.stButton>button{
    width:100% !important; border-radius:16px !important; height:58px !important;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%) !important;
    background-size: 200% auto !important; color:#0C1024 !important; font-size:19px !important; font-weight:800 !important; border:none !important;
    box-shadow: 0 14px 34px rgba(129,140,248,0.30) !important; transition: all 0.25s ease !important;
}
.stButton>button:hover{ background-position: right center !important; transform: translateY(-2px) !important; }

/* FIX: Forces all inner text elements to display extra bold and inherit full width alignment styling */
.stButton>button p, .stButton>button span div, .stButton>button div p { 
    color:#0C1024 !important; 
    font-weight:800 !important; 
}
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <span class="title-icon">🔐</span>
    <span class="title-text">Admin Panel</span>
</div>
""", unsafe_allow_html=True)
st.caption("Restricted access - Hospital admin only")

# ---------------- LOGIN GATE ----------------
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    with st.container(border=True):
        st.subheader("🔑 Admin Login")
        password_input = st.text_input("Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. Create columns to center the button nicely inside the card
        _, btn_col, _ = st.columns([1.5, 1, 1.5])
        
        with btn_col:
            # 2. Place the button inside the middle column
            if st.button("Login", type="primary", use_container_width=True):
                if password_input == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
    st.stop()

# ---------------- ADMIN FORM (only reached if authenticated) ----------------
col_a, col_b = st.columns([5, 1])
with col_a:
    st.success("Logged in as Admin")
with col_b:
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

with st.container(border=True):
    st.subheader("🏥 Update Hospital Status")
    st.caption("These numbers feed the staff Dashboard and the hospital status prediction model.")

    col1, col2 = st.columns(2)
    with col1:
        beds_available = st.number_input("Beds Available", min_value=0, value=15)
        total_doctors = st.number_input("Total Doctors", min_value=0, value=8)
        current_patients_ed = st.number_input("Current Patients in ED", min_value=0, value=42)
        total_nurses = st.number_input("Total Nurses", min_value=0, value=14)
    with col2:
        pending_lab_orders = st.number_input("Pending Lab Orders", min_value=0, value=6)
        pending_imaging_orders = st.number_input("Pending Imaging Orders", min_value=0, value=3)
        patients_boarding_ed = st.number_input("Patients Boarding in ED", min_value=0, value=5)
        avg_boarding_hours = st.number_input("Average Boarding Hours", min_value=0.0, value=2.5, step=0.5)

    # 1. Add visual breathing room between the inputs and the button
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Create asymmetric columns to tuck a premium-sized button right in the center
    _, submit_col, _ = st.columns([1.2, 1.6, 1.2])

    with submit_col:
        # 3. Render the smaller centered button securely
        submit = st.button("Save & Update Dashboard", type="primary", use_container_width=True)

    if submit:
        payload = {
            "beds_available": beds_available,
            "total_doctors": total_doctors,
            "current_patients_ed": current_patients_ed,
            "total_nurses": total_nurses,
            "pending_lab_orders": pending_lab_orders,
            "pending_imaging_orders": pending_imaging_orders,
            "patients_boarding_ed": patients_boarding_ed,
            "avg_boarding_hours": avg_boarding_hours,
        }
        try:
            response = requests.post(f"{BASE_URL}/admin/update_hospital_data", json=payload)
            response.raise_for_status()
            st.success("Hospital data updated. Dashboard will reflect this immediately.")
        except Exception:
            st.error("Backend is not running or the update failed.")
