import streamlit as st
import requests
from datetime import datetime
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(
    page_title="Patient Assistant After Triage",
    page_icon="🚑",
    layout="wide"
)

render_sidebar(3)

now = datetime.now()

NURSE_PATIENT_RATIO = 6
DOCTOR_PATIENT_RATIO = 12
BED_AVAILABLE = 1
ED_OVERCROWDED = 1
FLOOR_OR_CHAIR_CARE = 0
LABS_ORDERED = 1
IMAGING_ORDERED = 0

st.markdown("""
<style>
/* ================= GLOBAL / HEADER FIX ================= */
header[data-testid="stHeader"]{
    background: #0C1024 !important;
    background-image: none !important;
}
[data-testid="stToolbar"]{ background: transparent !important; }
html, body{
    background: #0C1024 !important;
}

/* ================= BACKGROUND — softer, "soothing" aurora on midnight slate ================= */
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

/* ================= TITLE EMOJI MASK FIX ================= */
.title-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 5px;
}
.title-icon {
    font-size: 2.8rem;
}
.title-text {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight:800 !important;
    letter-spacing:-0.02em;
    font-size:2.5rem !important;
}

h2, h3{ color:#EDEFFC !important; font-weight:700 !important; }
[data-testid="stCaptionContainer"]{ color:#9BA3C7 !important; font-size:15px !important; }

/* ================= SECTION CARDS ================= */
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:10px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

/* ================= LABELS ================= */
.stSelectbox label p, .stSlider label p, .stRadio label p, [data-testid="stWidgetLabel"] p{
    color:#C3CAE8 !important;
    font-weight:700 !important;
    font-size:14.5px !important;
}

/* ================= SELECT BOX ================= */
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
div[data-baseweb="select"] div{
    background: transparent !important;
    color:#EEF1FB !important;
}
div[data-baseweb="select"] input{
    color:#EEF1FB !important;
}
div[data-baseweb="select"] svg{ fill:#2DD4BF !important; }

/* Dropdown menu */
ul[data-baseweb="menu"], div[data-baseweb="popover"] ul, div[data-baseweb="popover"] div[role="listbox"]{
    background:#141A33 !important;
}
ul[data-baseweb="menu"] li, li[data-baseweb="menu-item"], div[role="listbox"] div{
    background:#141A33 !important;
    color:#EEF1FB !important;
}
li[data-baseweb="menu-item"]:hover, li[aria-selected="true"], div[role="option"]:hover{
    background: rgba(45,212,191,0.16) !important;
    color:#2DD4BF !important;
}

/* ================= SLIDER ================= */
.stSlider [data-baseweb="slider"] > div > div{ background: rgba(255,255,255,0.12) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"]{
    background-color:#F472B6 !important;
    box-shadow:0 0 0 6px rgba(244,114,182,0.20) !important;
    border: 2px solid #ffffff !important;
}
.stSlider [data-baseweb="slider"] > div > div > div{
    background: linear-gradient(90deg, #2DD4BF, #818CF8) !important;
}
[data-testid="stTickBar"] p, [data-testid="stThumbValue"]{ color:#EEF1FB !important; font-weight:700 !important; }
[data-testid="stThumbValue"]{ background:#F472B6 !important; border-radius:8px !important; padding:2px 8px !important; }

/* ================= RADIO (Clean Streamlit Default) ================= */
div[role="radiogroup"]{ gap:12px; }
div[role="radiogroup"] label{
    background:transparent !important; border:none !important; box-shadow:none !important; padding:2px 0 !important;
}
div[role="radiogroup"] label p{ color:#E5E7EB !important; font-weight:600 !important; }
input[type="radio"]:checked{ accent-color:#22C55E !important; }
input[type="radio"]{ filter:hue-rotate(90deg); }

/* ================= BUTTON ================= */
.stButton>button{
    width:100%; border-radius:16px; height:58px;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%);
    background-size: 200% auto; color:#0C1024; font-size:19px; font-weight:800; border:none;
    box-shadow: 0 14px 34px rgba(129,140,248,0.30); transition: all 0.25s ease;
}
.stButton>button:hover{ background-position: right center; transform: translateY(-2px); key-box-shadow: 0 18px 42px rgba(244,114,182,0.35); }
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }

/* ================= ERROR BANNER ================= */
div[data-testid="stAlertContentError"]{ color:#FCA5A5 !important; font-weight:700 !important; }

/* ================= CUSTOM STAT CARDS ================= */
.stat-card{
    background: rgba(255,255,255,0.045); border:1px solid rgba(255,255,255,0.10); border-radius:18px;
    padding:16px 18px; display:flex; align-items:center; gap:14px; backdrop-filter: blur(14px);
    box-shadow: 0 14px 34px rgba(0,0,0,0.3); margin-bottom:14px;
}
.stat-icon{
    width:46px; height:46px; border-radius:13px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-size:20px;
}
.stat-label{ font-size:12px; color:#9BA3C7; margin-bottom:3px; font-weight:600; }
.stat-val{ font-size:19px; font-weight:800; color:#EEF1FB; }

/* ================= RESULT CARDS WITH RING ================= */
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

div[role="radiogroup"] input[type="radio"]{ accent-color:#2DD4BF !important; }
div[role="radiogroup"] svg circle, div[role="radiogroup"] svg path{ stroke:#2DD4BF !important; fill:#2DD4BF !important; }
</style>
""", unsafe_allow_html=True)

# Custom aligned title wrapper
st.markdown("""
<div class="title-container">
    <span class="title-icon">🚑</span>
    <span class="title-text">Patient Assistant After Triage</span>
</div>
""", unsafe_allow_html=True)
st.caption("Clinical Decision Support After Triage Assessment")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background:rgba(45,212,191,0.16); color:#2DD4BF;">📅</div>
            <div><div class="stat-label">Day</div><div class="stat-val">{now.strftime('%A')}</div></div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background:rgba(129,140,248,0.16); color:#A5AEFA;">🕒</div>
            <div><div class="stat-label">Time</div><div class="stat-val">{now.strftime('%I:%M %p')}</div></div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background:rgba(52,211,153,0.16); color:#34D399;">🏥</div>
            <div><div class="stat-label">Emergency Department</div><div class="stat-val">Open</div></div>
        </div>
    """, unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("👤 Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Age", min_value=0, max_value=100, value=30)
        sex = st.selectbox("Sex", ["male", "female"])
    with col2:
        arrival_mode = st.selectbox("Arrival Mode", ["walk_in", "ambulance"])
        chronic_illness = st.selectbox("Chronic Illness", ["No", "Yes"])

with st.container(border=True):
    st.subheader("👨🏻‍⚕️ Triage Information")
    col3, col4 = st.columns(2)
    with col3:
        triage_category = st.selectbox("Triage Category", ["non_urgent", "standard", "urgent", "very_urgent", "emergency"])
    with col4:
        chief_complaint = st.selectbox("Chief Complaint", ["abdominal_pain", "cardiovascular", "fever_infection", "neurological", "obstetric_gynae", "other", "poisoning", "respiratory", "surgical", "trauma"])

predict = st.button("Predict", type="primary", use_container_width=True)

wait_time = "__"
doctor_wait = "__"
crowd_level = "Waiting"

if predict:
    with st.spinner("Generating predictions..."):
        now = datetime.now()
        payload = {
            "age": age, "sex": sex, "arrival_mode": arrival_mode, "time_of_day": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A").lower(), "chief_complaint": chief_complaint,
            "chronic_illness": 1 if chronic_illness == "Yes" else 0, "ed_overcrowded": ED_OVERCROWDED,
            "bed_available": BED_AVAILABLE, "floor_or_chair_care": FLOOR_OR_CHAIR_CARE,
            "nurse_patient_ratio": NURSE_PATIENT_RATIO, "doctor_patient_ratio": DOCTOR_PATIENT_RATIO,
            "labs_ordered": LABS_ORDERED, "imaging_ordered": IMAGING_ORDERED
        }
        try:
            response = requests.post("http://127.0.0.1:8000/predict_waittime", json=payload)
            wait_time = response.json()["estimated_wait_time"]

            doctor_payload = payload.copy()
            doctor_payload["triage_performed"] = 1
            doctor_payload["triage_category"] = triage_category
            doctor_payload["wait_triage_min"] = wait_time

            response = requests.post("http://127.0.0.1:8000/predict_doctor_wait", json=doctor_payload)
            doctor_wait = response.json()["estimated_doctor_wait"]

            if wait_time < 20: crowd_level = "🟢 Low"
            elif wait_time < 40: crowd_level = "🟠 Moderate"
            else: crowd_level = "🔴 High"
        except Exception:
            st.error("Backend is not running.")

def ring_pct(value, cap):
    try: return max(0, min(100, (float(value) / cap) * 100))
    except (ValueError, TypeError): return 0

wait_pct = ring_pct(wait_time, 60)
doc_pct = ring_pct(doctor_wait, 40)
crowd_color = {"🟢 Low": "#34D399", "🟠 Moderate": "#FBBF6E", "🔴 High": "#F87171"}.get(crowd_level, "#818CF8")
crowd_pct = {"🟢 Low": 33, "🟠 Moderate": 66, "🔴 High": 100}.get(crowd_level, 0)

if predict:
    with st.container(border=True):
        st.subheader("📊 Prediction Results")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="ring-card">
                <div class="ring" style="background:conic-gradient(#818CF8 0% {doc_pct}%, rgba(255,255,255,0.08) {doc_pct}% 100%);">
                    <div class="ring-inner"><div class="ring-num">{doctor_wait}</div><div class="ring-sub">min</div></div>
                </div>
                <div class="result-label">👨‍⚕️ Doctor Wait</div>
            </div>
        """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="ring-card">
                <div class="ring" style="background:conic-gradient({crowd_color} 0% {crowd_pct}%, rgba(255,255,255,0.08) {crowd_pct}% 100%);">
                    <div class="ring-inner"><div class="ring-num" style="font-size:15px;">{crowd_level.split(' ')[-1] if crowd_level != "Waiting" else "—"}</div></div>
                </div>
                <div class="result-label">📈 Crowd Level</div>
            </div>
        """, unsafe_allow_html=True)

        hospital_status = "Functional"
        if crowd_level == "🟠 Moderate": hospital_status = "Overcrowded"
        elif crowd_level == "🔴 High": hospital_status = "Overwhelmed"

        risk_payload = {
            "age": age, "chronic_illness": 1 if chronic_illness == "Yes" else 0,
            "triage_category": triage_category, "hospital_status": hospital_status,
            "bed_available": BED_AVAILABLE, "ed_overcrowded": ED_OVERCROWDED
        }
        try:
            response = requests.post("http://127.0.0.1:8000/admission_risk", json=risk_payload)
            risk_result = response.json()
            risk_score = risk_result["risk_score"]
            max_score = risk_result["max_score"]
            risk_label = risk_result["admission_risk"]
            recommendation = risk_result["recommendation"]

            if "Low" in risk_label: risk_color = "#34D399"
            elif "Moderate" in risk_label: risk_color = "#FBBF6E"
            else: risk_color = "#F87171"
            risk_pct = (risk_score / max_score) * 100
        except Exception:
            pass