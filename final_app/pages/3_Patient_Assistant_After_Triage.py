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
    page_icon="ROOM",
    layout="wide"
)
render_sidebar(3)

now = datetime.now()

# Shared Environment Parameters Defaults
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
    font-weight:800 !important;
    letter-spacing:-0.02em;
    font-size:2.5rem !important;
}

h2, h3, h4{ color:#EDEFFC !important; font-weight:700 !important; }
[data-testid="stCaptionContainer"]{ color:#9BA3C7 !important; font-size:15px !important; }

div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:10px;
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
.stButton>button:hover{ background-position: right center; transform: translateY(-2px); key-box-shadow: 0 18px 42px rgba(244,114,182,0.35); }
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }

.ring-card{
    background: rgba(255,255,255,0.045); border:1px solid rgba(255,255,255,0.10); border-radius:20px;
    padding:22px; text-align:center; backdrop-filter: blur(16px); box-shadow: 0 16px 40px rgba(0,0,0,0.3);
    height: 100%;
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
    <span class="title-icon">🚑</span>
    <span class="title-text">Patient Assistant After Triage</span>
</div>
""", unsafe_allow_html=True)
st.caption("Clinical Decision Support After Triage Assessment")

BASE_URL = "https://mediassist-ai-68lg.onrender.com"

raw_admin_metrics = None
h_status = "Functional"

try:
    response = requests.get(f"{BASE_URL}/admin/hospital_data")
    response.raise_for_status()
    raw_admin_data = response.json()
except Exception:
    raw_admin_data = None

if raw_admin_data and raw_admin_data.get("has_data"):
    raw_admin_metrics = raw_admin_data["admin_data"]
    h_status = raw_admin_data["predicted_status"]
    
    beds_val = int(raw_admin_metrics["beds_available"])
    if beds_val > 10: bed_status, bed_color = "🟢 Available", "#34D399"
    elif beds_val > 0: bed_status, bed_color = "🟠 Limited", "#FBBF6E"
    else: bed_status, bed_color = "🔴 Full", "#F87171"
    
    docs = int(raw_admin_metrics["total_doctors"])
    nurses = int(raw_admin_metrics["total_nurses"])
    patients = int(raw_admin_metrics["current_patients_ed"])
    BOARDING_IN_ED = int(raw_admin_metrics["patients_boarding_ed"])
    DOCTOR_PATIENT_RATIO = (patients / docs) if docs > 0 else patients
    NURSE_PATIENT_RATIO = (patients / nurses) if nurses > 0 else patients
    
    doc_status, doc_color = ("🟢 Available", "#34D399") if DOCTOR_PATIENT_RATIO < 4 else ("🟠 Busy", "#FBBF6E")
    
    if NURSE_PATIENT_RATIO < 2: nurse_status, nurse_color = "🟢 Normal Load", "#34D399"
    elif NURSE_PATIENT_RATIO < 4: nurse_status, nurse_color = "🟠 Moderate Load", "#FBBF6E"
    else: nurse_status, nurse_color = "🔴 High Load", "#F87171"
    
    last_update_str = raw_admin_data["admin_data"]["last_updated"].split("•")[-1].strip()
    
    BED_AVAILABLE = 1 if int(raw_admin_metrics["beds_available"]) > 0 else 0
    ED_OVERCROWDED = 1 if h_status in ["Overcrowded", "Overwhelmed"] else 0
    FLOOR_OR_CHAIR_CARE = 0
    LABS_ORDERED = 1 if int(raw_admin_metrics["pending_lab_orders"]) > 0 else 0
    IMAGING_ORDERED = 1 if int(raw_admin_metrics["pending_imaging_orders"]) > 0 else 0
else:
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

triage_clean_to_raw = {"Non Urgent": "non_urgent", "Standard": "standard", "Urgent": "urgent", "Very Urgent": "very_urgent", "Emergency": "emergency"}
triage_raw_to_clean = {v: k for k, v in triage_clean_to_raw.items()}

complaint_clean_to_raw = {
    "Abdominal Pain": "abdominal_pain", 
    "Cardiovascular": "cardiovascular", 
    "Fever Infection": "fever_infection", 
    "Neurological": "neurological", 
    "Obstetric Gynae": "obstetric_gynae", 
    "Other": "other", 
    "Poisoning": "poisoning", 
    "Respiratory": "respiratory", 
    "Surgical": "surgical", 
    "Trauma": "trauma"
}
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

with st.container(border=True):
    st.subheader("👨🏻‍⚕️ Triage Information")
    col3, col4 = st.columns(2)
    with col3:
        triage_opts = list(triage_clean_to_raw.keys())
        saved_raw_tri = st.session_state.get("triage_category", "standard")
        triage_idx = triage_opts.index(triage_raw_to_clean.get(saved_raw_tri, "Standard"))
        chosen_triage = st.selectbox("Triage Category", triage_opts, index=triage_idx)
        st.session_state.triage_category = triage_clean_to_raw[chosen_triage]
    with col4:
        complaint_opts = list(complaint_clean_to_raw.keys())
        saved_raw_comp = st.session_state.get("chief_complaint", "abdominal_pain")
        complaint_idx = complaint_opts.index(complaint_raw_to_clean.get(saved_raw_comp, "Abdominal Pain"))
        chosen_complaint = st.selectbox("Chief Complaint", complaint_opts, index=complaint_idx)
        st.session_state.chief_complaint = complaint_clean_to_raw[chosen_complaint]

st.write("")

# 🚨 EMERGENCY ALERT NOTICE BOX
st.markdown("""
<div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 18px; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15);">
    <h4 style="color:#EF4444; margin: 0 0 8px 0; font-weight:800; font-size: 16px; display: flex; align-items: center; gap: 8px;">
        🚨 EMERGENCY ALERT NOTICE
    </h4>
    <p style="color:#EEF1FB; margin: 0 0 8px 0; font-size: 13.5px; font-weight: 600;">
        If you are experiencing any of the following immediate life-threatening events:
    </p>
    <div style="display: flex; gap: 40px; color:#FCA5A5; font-size: 13.5px; font-weight: 700; margin-left: 10px; margin-bottom: 8px;">
        <div>• Acute Chest Pain</div>
        <div>• Severe Active Bleeding</div>
        <div>• Sudden Difficulty Breathing</div>
    </div>
    <p style="color:#C3CAE8; margin: 0; font-size: 12.5px; font-style: italic;">
        Please inform the nursing reception staff immediately for priority emergency care placement.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

predict = st.button("Predict", type="primary", use_container_width=True)

if 8 <= now.hour < 12:
    time_of_day = "morning_08_12"

elif 12 <= now.hour < 18:
    time_of_day = "afternoon_12_18"

elif 18 <= now.hour < 24:
    time_of_day = "evening_18_00"

else:
    time_of_day = "night_00_08"

if predict:
    with st.spinner("Generating predictions..."):
        now = datetime.now()

        payload = {
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
            "nurse_patient_ratio": int(NURSE_PATIENT_RATIO),  # Wrapped in int()
            "doctor_patient_ratio": int(DOCTOR_PATIENT_RATIO), # Wrapped in int()
            "labs_ordered": int(LABS_ORDERED), 
            "imaging_ordered": int(IMAGING_ORDERED)
        }
        try:
            response = requests.post(f"{BASE_URL}/predict_waittime", json=payload)
            wait_time = response.json()["estimated_wait_time"]

            doctor_payload = payload.copy()
            doctor_payload["triage_performed"] = 1
            doctor_payload["triage_category"] = st.session_state.triage_category
            doctor_payload["wait_triage_min"] = wait_time

            response = requests.post(f"{BASE_URL}/predict_doctor_wait", json=doctor_payload)
            doctor_wait = response.json()["estimated_doctor_wait"]

            if wait_time < 20:
                raw_crowd = "Low"
            elif wait_time < 40:
                raw_crowd = "Moderate"
            else:
                raw_crowd = "High"

            if raw_admin_metrics:

                hospital_status_payload = {
                    "bed_available": 1 if int(raw_admin_metrics["beds_available"]) > 0 else 0,
                    "nurse_patient_ratio": int(NURSE_PATIENT_RATIO),
                    "doctor_patient_ratio": int(DOCTOR_PATIENT_RATIO),
                    "boarding_in_ed": int(raw_admin_metrics["patients_boarding_ed"]),
                    "boarding_hrs": float(raw_admin_metrics["avg_boarding_hours"]),
                    "labs_ordered": LABS_ORDERED,
                    "imaging_ordered": IMAGING_ORDERED,
                    "wait_doctor_min": float(doctor_wait),
                    "arrival_mode": st.session_state.arrival_mode,
                    "time_of_day": time_of_day,
                    "day_of_week": "weekend" if (now.weekday() >= 5) else "weekday"
                }
                status_resp = requests.post(f"{BASE_URL}/predict_hospital_status", json=hospital_status_payload)
                hospital_status_prediction = status_resp.json()["hospital_status"]
            else:
                hospital_status_prediction = "Functional"
                if wait_time >= 40: hospital_status_prediction = "Overwhelmed"
                elif wait_time >= 20: hospital_status_prediction = "Overcrowded"

            # --- Change 2: Updated Hospital Status Crowd Logic ---
            if doctor_wait < 45 and hospital_status_prediction == "Functional":
                crowd_level = "🟢 Low"
            elif doctor_wait >= 70 or hospital_status_prediction == "Overwhelmed":
                crowd_level = "🔴 High"
            else:
                crowd_level = "🟠 Moderate"

            admission_payload = {
                "age": int(st.session_state.age),
                "sex": st.session_state.sex.lower(),
                "arrival_mode": st.session_state.arrival_mode,
                "time_of_day": time_of_day,
                "day_of_week": "weekend" if now.weekday() >= 5 else "weekday",
                "triage_category": st.session_state.triage_category,
                "chief_complaint": st.session_state.chief_complaint,
                "chronic_illness": 1 if st.session_state.chronic_illness == "Yes" else 0,
                "ed_overcrowded": ED_OVERCROWDED,
                "bed_available": BED_AVAILABLE,
                "nurse_patient_ratio": int(NURSE_PATIENT_RATIO),
                "doctor_patient_ratio": int(DOCTOR_PATIENT_RATIO),
                "wait_doctor_min": int(doctor_wait)
            }

            response = requests.post(
                f"{BASE_URL}/admission_risk",
                json=admission_payload
            )

            result = response.json()

            risk_score = result["risk_score"]
            risk_label = result["admission_risk"]
            recommendation = result["recommendation"]

            def ring_pct(value, cap):
                try: return max(0, min(100, (float(value) / cap) * 100))
                except (ValueError, TypeError): return 0

            doc_pct = ring_pct(doctor_wait, 80)
            
            crowd_color = {"🟢 Low": "#34D399", "🟠 Moderate": "#FBBF6E", "🔴 High": "#F87171"}.get(crowd_level, "#818CF8")
            crowd_pct = {"🟢 Low": 33, "🟠 Moderate": 66, "🔴 High": 100}.get(crowd_level, 0)
            
            risk_color = {"🟢 Low": "#34D399", "🟡 Moderate": "#FBBF6E", "🔴 High": "#F87171"}.get(risk_label, "#818CF8")
            risk_pct = (risk_score / 10.0) * 100

            with st.container(border=True):
                st.subheader("📊 Prediction Results")
                st.columns(3)
                c1, c2, c3 = st.columns(3)
                
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
                            <div class="ring-inner"><div class="ring-num" style="font-size:15px;">{crowd_level.split(' ')[-1]}</div></div>
                        </div>
                        <div class="result-label">📈 Crowd Level</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # --- Change 1: Updated with c3 layout alignment ---
                with c3:
                    st.markdown(f"""
                    <div class="ring-card">
                        <div class="ring" style="background:conic-gradient({risk_color} 0% {risk_pct}%, rgba(255,255,255,0.08) {risk_pct}% 100%);">
                            <div class="ring-inner"><div class="ring-num">{int(risk_score) if risk_score % 1 == 0 else risk_score}/10</div><div class="ring-sub">Score</div></div>
                        </div>
                        <div class="result-label">🚨 Admission Likelihood</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Clinical Assessment Card
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.045); border: 1px solid rgba(255,255,255,0.10); border-radius: 18px; padding: 20px; backdrop-filter: blur(14px); box-shadow: 0 14px 34px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 20px;">
                    <div style="font-size: 2.3rem; flex-shrink: 0;">🏥</div>
                    <div>
                        <h4 style="color:{risk_color}; margin: 0 0 6px 0; font-weight:700; font-size: 19px; display: flex; align-items: center; gap: 8px;">
                            Clinical Assessment: {risk_label} Admission Likelihood
                        </h4>
                        <p style="color:#C3CAE8; margin: 0; font-size: 14.5px; line-height: 1.5;">{recommendation}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 📋 NEXT STEP COMPONENT HIERARCHY
                st.markdown("""
                <br>
                <div style="background: rgba(129, 140, 248, 0.06); border: 1px solid rgba(129, 140, 248, 0.25); border-radius: 18px; padding: 20px; backdrop-filter: blur(14px); box-shadow: 0 14px 34px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 20px;">
                    <div style="font-size: 2.3rem; flex-shrink: 0;">📋</div>
                    <div>
                        <h4 style="color:#818CF8; margin: 0 0 6px 0; font-weight:700; font-size: 17px;">Next Steps for Care Progression</h4>
                        <div style="color:#C3CAE8; font-size: 14px; line-height: 1.6; font-weight: 500;">
                            1. Please remain seated comfortably in the triage waiting area until your name is broadcast over the loudspeaker system.<br>
                            2. Keep your mobile communication devices nearby and active for automated placement alerts.<br>
                            3. Ensure any physical copies of past medication prescriptions or lab records are organized and ready for primary physician intake review.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

            if 'response' in locals():
                try:
                    st.write(response.status_code)
                    st.write(response.text)
                except:
                    pass