import streamlit as st
import requests
from datetime import datetime
import sys
import os

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
.title-icon {
    font-size: 2.8rem;
}
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
div[data-baseweb="select"] div{
    background: transparent !important;
    color:#EEF1FB !important;
}
div[data-baseweb="select"] input{ color:#EEF1FB !important; }
div[data-baseweb="select"] input::placeholder { color: #ffffff !important; }
div[data-baseweb="select"] svg{ fill:#2DD4BF !important; }

/* PREMIUM DROPDOWN HOVER STYLING UPGRADES */
div[data-baseweb="popover"] {
    background-color: #0E132B !important;
}
div[data-baseweb="popover"] ul {
    background-color: #0E132B !important;
}
div[data-baseweb="popover"] li {
    background-color: #0E132B !important;
    color: #EEF1FB !important;
    transition: all 0.2s ease;
}
div[data-baseweb="popover"] li:hover {
    background-color: #818CF8 !important;
    color: #ffffff !important;
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
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }

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

BASE_URL = "http://127.0.0.1:8000"

try:
    response = requests.get(f"{BASE_URL}/admin/hospital_data")
    response.raise_for_status()
    raw_admin_data = response.json()
except Exception:
    raw_admin_data = None

if raw_admin_data and raw_admin_data.get("has_data"):
    metrics = raw_admin_data["admin_data"]
    h_status = raw_admin_data["predicted_status"]
    
    beds_val = int(metrics["beds_available"])
    if beds_val > 10: bed_status, bed_color = "🟢 Available", "#34D399"
    elif beds_val > 0: bed_status, bed_color = "🟠 Limited", "#FBBF6E"
    else: bed_status, bed_color = "🔴 Full", "#F87171"
    
    docs = int(metrics["total_doctors"])
    nurses = int(metrics["total_nurses"])
    patients = int(metrics["current_patients_ed"])
    
    DOCTOR_PATIENT_RATIO = (patients / docs) if docs > 0 else patients
    NURSE_PATIENT_RATIO = (patients / nurses) if nurses > 0 else patients
    
    doc_status, doc_color = ("🟢 Available", "#34D399") if DOCTOR_PATIENT_RATIO < 4 else ("🟠 Busy", "#FBBF6E")
    
    if NURSE_PATIENT_RATIO < 2: nurse_status, nurse_color = "🟢 Normal Load", "#34D399"
    elif NURSE_PATIENT_RATIO < 4: nurse_status, nurse_color = "🟠 Moderate Load", "#FBBF6E"
    else: nurse_status, nurse_color = "🔴 High Load", "#F87171"
    
    last_update_str = metrics["last_updated"].split("•")[-1].strip()
    BED_AVAILABLE = int(metrics["beds_available"])
    ED_OVERCROWDED = 1 if h_status in ["Overcrowded", "Overwhelmed"] else 0
    FLOOR_OR_CHAIR_CARE = 0
    LABS_ORDERED = int(metrics["pending_lab_orders"])
    IMAGING_ORDERED = int(metrics["pending_imaging_orders"])
else:
    h_status = "Functional"
    bed_status, bed_color = "🟢 Available", "#34D399"
    doc_status, doc_color = "🟢 Available", "#34D399"
    nurse_status, nurse_color = "🟠 Moderate Load", "#FBBF6E"
    last_update_str = now.strftime('%I:%M %p')
    
    NURSE_PATIENT_RATIO = 6
    DOCTOR_PATIENT_RATIO = 12
    BED_AVAILABLE = 1
    ED_OVERCROWDED = 1
    FLOOR_OR_CHAIR_CARE = 0
    LABS_ORDERED = 1
    IMAGING_ORDERED = 0

status_mapping = {
    "Functional": ("🟢 Functional", "Minimal Delay", "#34D399"),
    "Overcrowded": ("🟠 Overcrowded", "Moderate Delay", "#FBBF6E"),
    "Overwhelmed": ("🔴 Overwhelmed", "Significant Delay", "#F87171")
}
disp_status, disp_delay, status_color = status_mapping.get(h_status, ("🟢 Functional", "Minimal Delay", "#34D399"))

c_a, c_b, c_c, c_d, c_e = st.columns(5)
with c_a:
    st.markdown(f'<div class="info-title">🏥 Hospital Status</div><div class="info-value" style="color:{status_color};">{disp_status}</div><div style="font-size:11px; color:#9BA3C7;">{disp_delay}</div>', unsafe_allow_html=True)
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
        st.session_state.age = st.slider("Age", min_value=0, max_value=100, value=st.session_state.get("age", 30))
        
        sex_opts = ["Male", "Female"]
        sex_idx = sex_opts.index(st.session_state.get("sex", "Male"))
        chosen_sex = st.selectbox("Sex", sex_opts, index=sex_idx)
        st.session_state.sex = chosen_sex
        
        complaint_opts = list(complaint_clean_to_raw.keys())
        saved_raw_comp = st.session_state.get("chief_complaint", "abdominal_pain")
        complaint_idx = complaint_opts.index(complaint_raw_to_clean.get(saved_raw_comp, "Abdominal Pain"))
        chosen_complaint = st.selectbox("Chief Complaint", complaint_opts, index=complaint_idx)
        st.session_state.chief_complaint = complaint_clean_to_raw[chosen_complaint]
        
    with col2:
        arrival_opts = list(arrival_clean_to_raw.keys())
        saved_raw_arr = st.session_state.get("arrival_mode", "walk_in")
        arrival_idx = arrival_opts.index(arrival_raw_to_clean.get(saved_raw_arr, "Walk In"))
        chosen_arrival = st.selectbox("Arrival Mode", arrival_opts, index=arrival_idx)
        st.session_state.arrival_mode = arrival_clean_to_raw[chosen_arrival]
        
        ill_opts = ["No", "Yes"]
        ill_idx = ill_opts.index(st.session_state.get("chronic_illness", "No"))
        chosen_ill = st.selectbox("Chronic Illness", ill_opts, index=ill_idx)
        st.session_state.chronic_illness = chosen_ill

st.write("")

st.markdown("""
<div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 18px; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15);">
    <h4 style="color:#EF4444; margin: 0 0 8px 0; font-weight:800; font-size: 16px; display: flex; align-items: center; gap: 8px;">
        🚨 EMERGENCY ALERT NOTICE
    </h4>
    <p style="color:#EEF1FB; margin: 0 0 8px 0; font-size: 13.5px; font-weight: 600;">
        If you or the patient are currently experiencing any of the following critical high-risk symptoms:
    </p>
    <div style="display: flex; gap: 40px; color:#FCA5A5; font-size: 13.5px; font-weight: 700; margin-left: 10px; margin-bottom: 8px;">
        <div>• Chest Pain / Pressure</div>
        <div>• Severe Uncontrolled Bleeding</div>
        <div>• Acute Difficulty Breathing</div>
    </div>
    <p style="color:#C3CAE8; margin: 0; font-size: 12.5px; font-style: italic;">
        Please bypass this assessment application and inform the medical reception desk or emergency personnel immediately.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

predict_clicked = st.button("Predict", type="primary", use_container_width=True)

if predict_clicked:
    with st.spinner("Generating predictions..."):
        now = datetime.now()
        
        wait_payload = {
            "age": st.session_state.age, 
            "sex": st.session_state.sex.lower(), 
            "arrival_mode": st.session_state.arrival_mode, 
            "time_of_day": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A").lower(), 
            "chief_complaint": st.session_state.chief_complaint,
            "chronic_illness": 1 if st.session_state.chronic_illness == "Yes" else 0, 
            "ed_overcrowded": ED_OVERCROWDED,
            "bed_available": BED_AVAILABLE, "floor_or_chair_care": FLOOR_OR_CHAIR_CARE,
            "nurse_patient_ratio": NURSE_PATIENT_RATIO, "doctor_patient_ratio": DOCTOR_PATIENT_RATIO,
            "labs_ordered": LABS_ORDERED, "imaging_ordered": IMAGING_ORDERED
        }
        
        try:
            wait_response = requests.post(f"{BASE_URL}/predict_waittime", json=wait_payload)
            wait_time = wait_response.json()["estimated_wait_time"]

            # Smart Multi-Variable Crowd Logic
            if wait_time < 20 and h_status == "Functional":
                crowd_level = "🟢 Low"
            elif wait_time >= 40 or h_status == "Overwhelmed":
                crowd_level = "🔴 High"
            else:
                crowd_level = "🟠 Moderate"

        except Exception:
            wait_time = 0
            crowd_level = "Waiting"
            st.error("Backend wait-time engine is not responding.")

        def ring_pct(value, cap):
            try: return max(0, min(100, (float(value) / cap) * 100))
            except (ValueError, TypeError): return 0

        wait_pct = ring_pct(wait_time, 60)
        crowd_color = {"🟢 Low": "#34D399", "🟠 Moderate": "#FBBF6E", "🔴 High": "#F87171"}.get(crowd_level, "#818CF8")
        crowd_pct = {"🟢 Low": 33, "🟠 Moderate": 66, "🔴 High": 100}.get(crowd_level, 0)

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
                        <div class="ring-inner"><div class="ring-num" style="font-size:15px;">{crowd_level.split(' ')[-1] if crowd_level != "Waiting" else "—"}</div></div>
                    </div>
                    <div class="result-label">📈 Crowd Level</div>
                </div>
                """, unsafe_allow_html=True)
            
            if wait_time >= 45:
                st.markdown("""
                <br>
                <div style="background: rgba(244, 114, 182, 0.08); border: 1px solid rgba(244, 114, 182, 0.3); border-radius: 18px; padding: 20px; backdrop-filter: blur(14px); box-shadow: 0 14px 34px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 20px;">
                    <div style="font-size: 2.3rem; flex-shrink: 0;">ℹ️</div>
                    <div>
                        <h4 style="color:#F472B6; margin: 0 0 6px 0; font-weight:700; font-size: 17px;">High Patient Volume Alert</h4>
                        <p style="color:#C3CAE8; margin: 0 0 8px 0; font-size: 14px; line-height: 1.5;">
                            The Emergency Department is currently experiencing high patient volume layouts. If your present medical condition is non-life-threatening, consider utilizing these alternative care vectors for significantly faster turnaround assistance:
                        </p>
                        <div style="color:#EEF1FB; font-size: 13.5px; font-weight: 700; margin-left: 15px;">
                            • Walk-In Nearby Urgent Care Center Facilities<br>
                            • On-Demand Digital Telehealth Consultation Portals
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)