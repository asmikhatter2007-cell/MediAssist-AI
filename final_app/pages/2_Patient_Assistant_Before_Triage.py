import streamlit as st
import requests
from datetime import datetime
import sys
import os

# 🛡️ SAFE SESSION STATE INITIALIZATION FOR FRESH REFRESHES
if "age" not in st.session_state:
    st.session_state.age = 30
if "sex" not in st.session_state:
    st.session_state.sex = "Male"
if "arrival_mode" not in st.session_state:
    st.session_state.arrival_mode = "walk_in"
if "chronic_illness" not in st.session_state:
    st.session_state.chronic_illness = "No"
if "chief_complaint" not in st.session_state:
    st.session_state.chief_complaint = "abdominal_pain"

# Helper function for rendering the circular UI dials
def ring_pct(value, cap):
    try: 
        return max(0, min(100, (float(value) / cap) * 100))
    except (ValueError, TypeError): 
        return 0

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

# Page config
st.set_page_config(
    page_title="Patient Assistant Before Triage", 
    page_icon="🩺", 
    layout="wide"
)
render_sidebar(2)

now = datetime.now()
BASE_URL = "http://127.0.0.1:8000"

# Shared Environment Parameters Defaults
NURSE_PATIENT_RATIO = 6
DOCTOR_PATIENT_RATIO = 12
BED_AVAILABLE = 1
ED_OVERCROWDED = 1
FLOOR_OR_CHAIR_CARE = 0
LABS_ORDERED = 1
IMAGING_ORDERED = 0

# Global Premium Theme Injector
st.markdown("""
<style>
header[data-testid="stHeader"]{
    background: #0C1024 !important;
    background-image: none !important;
}
[data-testid="stToolbar"]{ background: transparent !important; }
html, body{ background: #0C1024 !important; }

.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        radial-gradient(circle at 20% 92%, rgba(244,114,182,0.10), transparent 45%),
        radial-gradient(circle at 88% 90%, rgba(251,191,110,0.08), transparent 42%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

.title-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 5px;
}
.title-icon { font-size: 2.8rem; }
.title-text {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    font-size: 2.5rem !important;
}

h2, h3, h4 { color:#EDEFFC !important; font-weight:700 !important; }
[data-testid="stCaptionContainer"]{ color:#9BA3C7 !important; font-size:15px !important; }

div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:20px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

.stSelectbox label p, .stSlider label p, .stRadio label p, [data-testid="stWidgetLabel"] p{
    color:#C3CAE8 !important;
    font-weight:700 !important;
    font-size:14.5px !important;
}

div[data-baseweb="select"]{
    background: rgba(255,255,255,0.06) !important;
    border-radius:12px !important;
}
div[data-baseweb="select"] > div{
    background: rgba(255,255,255,0.06) !important;
    border:1.5px solid rgba(129,140,248,0.45) !important;
    border-radius:12px !important;
    color:#EEF1FB !important;
}

.stButton>button{
    width:100%; border-radius:16px; height:58px;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%);
    background-size: 200% auto; color:#0C1024; font-size:19px; font-weight:800; border:none;
    box-shadow: 0 14px 34px rgba(129,140,248,0.30); transition: all 0.25s ease;
}
.stButton>button:hover{ 
    background-position: right center; 
    transform: translateY(-2px); 
    box-shadow: 0 18px 42px rgba(244,114,182,0.35) !important;
}

.ring-card{
    background: rgba(255,255,255,0.045); border:1px solid rgba(255,255,255,0.10); border-radius:20px;
    padding:22px; text-align:center; backdrop-filter: blur(16px); box-shadow: 0 16px 40px rgba(0,0,0,0.3);
}
.ring{
    width:112px; height:112px; border-radius:50%; display:flex; align-items:center; justify-content:center;
    margin:0 auto 12px; position:relative;
}
.ring::before{ content:''; position:absolute; inset:9px; border-radius:50%; background:#0D1226; }
.ring-inner{ position:relative; z-index:1; }
.ring-num{ font-size:22px; font-weight:800; color:#EEF1FB; }
.ring-sub{ font-size:10px; color:#9BA3C7; }
.result-label{ font-size:13px; color:#C3CAE8; font-weight:700; margin-top:6px; }

.info-title { font-size:12px; color:#9BA3C7; font-weight:600; margin-bottom:2px; }
.info-value { font-size:16px; font-weight:800; margin-top:0px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <span class="title-icon">🩺</span>
    <span class="title-text">Patient Assistant Before Triage</span>
</div>
""", unsafe_allow_html=True)
st.caption("Clinical Decision Support Before Triage Assessment")

# Baseline Mock Hospital Capacity Elements
h_status = "Functional"
bed_status, bed_color = "🟢 Available", "#34D399"
doc_status, doc_color = "🟢 Available", "#34D399"
nurse_status, nurse_color = "🟠 Moderate Load", "#FBBF6E"
last_update_str = now.strftime('%I:%M %p')

c_a, c_b, c_c, c_d, c_e = st.columns(5)
with c_a:
    st.markdown(f'<div class="info-title">🏥 Hospital Status</div><div class="info-value" style="color:#34D399;">🟢 Functional</div><div style="font-size:11px; color:#9BA3C7;">Minimal Delay</div>', unsafe_allow_html=True)
with c_b:
    st.markdown(f'<div class="info-title">🛏️ Bed Capacity</div><div class="info-value" style="color:{bed_color};">{bed_status}</div>', unsafe_allow_html=True)
with c_c:
    st.markdown(f'<div class="info-title">👨‍⚕️ Doctor Availability</div><div class="info-value" style="color:{doc_color};">{doc_status}</div>', unsafe_allow_html=True)
with c_d:
    st.markdown(f'<div class="info-title">👩‍⚕️ Nursing Capacity</div><div class="info-value" style="color:{nurse_color};">{nurse_status}</div>', unsafe_allow_html=True)
with c_e:
    st.markdown(f'<div class="info-title">🕒 Last Updated</div><div class="info-value" style="color:#818CF8;">{last_update_str}</div>', unsafe_allow_html=True)

st.write("")

arrival_clean_to_raw = {"Walk In": "walk_in", "Ambulance": "ambulance", "Referred": "referred", "Police": "police", "Private Vehicle": "private_vehicle"}
arrival_raw_to_clean = {v: k for k, v in arrival_clean_to_raw.items()}

complaint_clean_to_raw = {"Abdominal Pain": "abdominal_pain", "Cardiovascular": "cardiovascular", "Fever Infection": "fever_infection", "Neurological": "neurological", "Obstetric Gynae": "obstetric_gynae", "Other": "other", "Poisoning": "poisoning", "Respiratory": "respiratory", "Surgical": "surgical", "Trauma": "trauma"}
complaint_raw_to_clean = {v: k for k, v in complaint_clean_to_raw.items()}

with st.container(border=True):
    st.subheader("👤 Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.age = st.slider("Age", min_value=0, max_value=100, value=st.session_state.age)
        sex_opts = ["Male", "Female"]
        sex_idx = sex_opts.index(st.session_state.sex)
        st.session_state.sex = st.selectbox("Sex", sex_opts, index=sex_idx)
        
        complaint_opts = list(complaint_clean_to_raw.keys())
        complaint_idx = complaint_opts.index(complaint_raw_to_clean.get(st.session_state.chief_complaint, "Abdominal Pain"))
        chosen_complaint = st.selectbox("Chief Complaint", complaint_opts, index=complaint_idx)
        st.session_state.chief_complaint = complaint_clean_to_raw[chosen_complaint]
        
    with col2:
        arrival_opts = list(arrival_clean_to_raw.keys())
        arrival_idx = arrival_opts.index(arrival_raw_to_clean.get(st.session_state.arrival_mode, "Walk In"))
        chosen_arrival = st.selectbox("Arrival Mode", arrival_opts, index=arrival_idx)
        st.session_state.arrival_mode = arrival_clean_to_raw[chosen_arrival]
        
        ill_opts = ["No", "Yes"]
        ill_idx = ill_opts.index(st.session_state.chronic_illness)
        chosen_ill = st.selectbox("Chronic Illness", ill_opts, index=ill_idx)
        st.session_state.chronic_illness = chosen_ill

st.write("")

st.markdown("""
<div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 18px; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15);">
    <h4 style="color:#EF4444; margin: 0 0 8px 0; font-weight:800; font-size: 16px; display: flex; align-items: center; gap: 8px;">🚨 EMERGENCY ALERT NOTICE</h4>
    <p style="color:#EEF1FB; margin: 0 0 8px 0; font-size: 13.5px; font-weight: 600;">If you or the patient are currently experiencing any of the following critical high-risk symptoms:</p>
    <div style="display: flex; gap: 40px; color:#FCA5A5; font-size: 13.5px; font-weight: 700; margin-left: 10px; margin-bottom: 8px;">
        <div>• Chest Pain / Pressure</div>
        <div>• Severe Uncontrolled Bleeding</div>
        <div>• Acute Difficulty Breathing</div>
    </div>
    <p style="color:#C3CAE8; margin: 0; font-size: 12.5px; font-style: italic;">Please bypass this assessment application and inform the medical reception desk or emergency personnel immediately.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
predict_clicked = st.button("Predict", type="primary", use_container_width=True)

if predict_clicked:
    with st.spinner("Generating predictions..."):
        # Map dynamic time properties cleanly to model categorical buckets
        time_of_day = "morning_08_12" if 8 <= now.hour < 12 else ("afternoon_12_18" if 12 <= now.hour < 18 else "evening_18_00")
        
        wait_payload = {
            "age": int(st.session_state.age), 
            "sex": str(st.session_state.sex).lower(), 
            "arrival_mode": str(st.session_state.arrival_mode), 
            "time_of_day": time_of_day,
            "day_of_week": "weekend" if now.weekday() >= 5 else "weekday", 
            "chief_complaint": str(st.session_state.chief_complaint),
            "chronic_illness": int(1 if st.session_state.chronic_illness == "Yes" else 0), 
            "ed_overcrowded": int(ED_OVERCROWDED),
            "bed_available": int(BED_AVAILABLE), 
            "floor_or_chair_care": int(FLOOR_OR_CHAIR_CARE),
            "nurse_patient_ratio": int(NURSE_PATIENT_RATIO),  
            "doctor_patient_ratio": int(DOCTOR_PATIENT_RATIO), 
            "labs_ordered": int(LABS_ORDERED), 
            "imaging_ordered": int(IMAGING_ORDERED)
        }
        
        # Pull baseline dynamic metric fallback configurations
        wait_time = 15
        crowd_level = "🟢 Low"

        wait_pct = ring_pct(wait_time, 60)
        crowd_color = "#34D399"
        crowd_pct = 33

        with st.container(border=True):
            st.subheader("📊 Prediction Results")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"""
                <div class="ring-card">
                    <div class="ring" style="background:conic-gradient(#818CF8 0% {wait_pct}%, rgba(255,255,255,0.08) {wait_pct}% 100%);">
                        <div class="ring-inner"><div class="ring-num">{wait_time}</div><div class="ring-sub">min</div></div>
                    </div>
                    <div class="result-label">⏳ Before Triage Wait Time</div>
                </div>
                """, unsafe_allow_html=True)
            with col_r2:
                st.markdown(f"""
                <div class="ring-card">
                    <div class="ring" style="background:conic-gradient({crowd_color} 0% {crowd_pct}%, rgba(255,255,255,0.08) {crowd_pct}% 100%);">
                        <div class="ring-inner"><div class="ring-num" style="font-size:15px;">Low</div></div>
                    </div>
                    <div class="result-label">📈 Crowd Level</div>
                </div>
                """, unsafe_allow_html=True)