import streamlit as st
from navigation import render_sidebar

# Page Configuration
st.set_page_config(
    page_title="MediAssist AI - Home",
    page_icon="🏥",
    layout="wide",
)
render_sidebar(0)

# Premium Global Style Injector
st.markdown("""
<style>
header[data-testid="stHeader"]{ background: #0C1024 !important; }
[data-testid="stToolbar"]{ background: transparent !important; }
html, body{ background: #0C1024 !important; }
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}

.title-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-bottom: 5px;
}
.title-icon { font-size: 3.5rem; }
.hero-title {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 3.5rem !important;
    margin-bottom: 0px;
    display: inline-block;
}
.hero-subtitle { color: #EDEFFC !important; font-weight: 700 !important; text-align: center; margin-top: 10px; font-size: 1.5rem; }
.hero-desc { text-align: center; font-size: 18px; color: #9BA3C7 !important; margin-bottom: 35px; }

div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius: 22px !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    padding: 24px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    height: 100%;
}
div[data-testid="stVerticalBlockBorderWrapper"] p { color: #EEF1FB !important; }
li { color: #C3CAE8 !important; margin-bottom: 6px; font-size: 14.5px; }
h3 { color: #EDEFFC !important; font-weight: 700 !important; margin-top: 5px; }
h4 { color: #2DD4BF !important; font-weight: 700 !important; margin-top: 5px; }

.tech-badge {
    display: inline-block;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 6px 14px;
    border-radius: 10px;
    margin: 4px;
    font-weight: 600;
    color: #2DD4BF;
}

.journey-node {
    background: rgba(129,140,248,0.08);
    border: 1px solid rgba(129,140,248,0.2);
    border-radius: 14px;
    padding: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- 🏥 HERO SECTION ---
st.markdown("""
<div class="title-container">
    <span class="title-icon">🏥</span>
    <h1 class="hero-title">MediAssist AI</h1>
</div>
""", unsafe_allow_html=True)
st.markdown('<h3 class="hero-subtitle">AI-Powered Emergency Department Decision Support System</h3>', unsafe_allow_html=True)
st.markdown('<p class="hero-desc">Improving emergency care through intelligent disease prediction, hospital resource monitoring, waiting time estimation, and admission support.</p>', unsafe_allow_html=True)

# --- 2️⃣ ABOUT THE SYSTEM ---
with st.container(border=True):
    st.markdown("### 🩺 About MediAssist AI")
    st.markdown("MediAssist AI is an intelligent healthcare assistance platform designed to support both patients and hospital staff throughout the emergency department journey. The system combines multiple machine learning models to provide disease prediction, specialist recommendation, hospital status prediction, waiting time estimation, and admission likelihood assessment, helping improve patient experience and emergency department efficiency.")

st.write("")

# --- 3️⃣ WHO CAN USE IT? ---
st.markdown("### 👥 Who Can Use MediAssist AI?")
col_u1, col_user2 = st.columns(2)
with col_u1:
    with st.container(border=True):
        st.markdown("#### 👤 Patient Services")
        st.markdown("""
        * 🧬 **Disease Predictor** — Review symptoms and check for likely illnesses
        * 👨‍⚕️ **Specialist Recommendation** — Find the appropriate clinical specialty
        * 🩺 **Before Triage Assistant** — Know what to expect before stepping inside
        * ⏳ **Waiting Time Estimation** — View personalized registration delays
        * 🏥 **Admission Guidance** — Understand clinic processing timelines
        """)
with col_user2:
    with st.container(border=True):
        st.markdown("#### 🏥 Hospital Services")
        st.markdown("""
        * ⚙️ **Administrative Resource Panel** — Configure and update facility data
        * 📊 **Live Operational Dashboard** — Monitor active real-time data queues
        * 🛏 **Bed Capacity Monitoring** — Keep precise tabs on available slots
        * 👨‍⚕️ **Staff Availability Tracking** — Observe shifts for active doctors and nurses
        * 📈 **Hospital Status Prediction** — Review AI-driven facility load forecasts
        """)

st.write("")

# --- 4️⃣ PATIENT JOURNEY ---
st.markdown("### 🔄 Patient Journey")
col_j1, col_j2, col_j3, col_j4, col_j5 = st.columns(5)
with col_j1:
    st.markdown('<div class="journey-node">🔍<br><b>Symptom Checker</b></div>', unsafe_allow_html=True)
with col_j2:
    st.markdown('<div class="journey-node">🩺<br><b>Before Triage</b></div>', unsafe_allow_html=True)
with col_j3:
    st.markdown('<div class="journey-node">🏥<br><b>Hospital Visit</b></div>', unsafe_allow_html=True)
with col_j4:
    st.markdown('<div class="journey-node">🚑<br><b>After Triage</b></div>', unsafe_allow_html=True)
with col_j5:
    st.markdown('<div class="journey-node">👨‍⚕️<br><b>Consultation</b></div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9BA3C7; margin-top: 15px; font-size: 14.5px;'>MediAssist AI supports patients throughout their emergency department journey—from symptom assessment to physician consultation.</p>", unsafe_allow_html=True)

st.write("")

# --- 5️⃣ KEY FEATURES ---
st.markdown("### 🌟 Core Features")
cf1, cf2, cf3 = st.columns(3)
with cf1:
    with st.container(border=True):
        st.markdown("#### 🔍 Disease Prediction")
        st.markdown("Analyzes symptom metrics to identify the most probable disease background.")
    with st.container(border=True):
        st.markdown("#### ⏳ Wait Time Prediction")
        st.markdown("Predicts triage registration processing times based on raw entrance volume.")
with cf2:
    with st.container(border=True):
        st.markdown("#### 🧑‍⚕️ Specialist Recommendation")
        st.markdown("Maps diagnostic targets to select the most appropriate department team.")
    with st.container(border=True):
        st.markdown("#### 👨‍⚕️ Doctor Wait Estimation")
        st.markdown("Forecasts minutes until final medical physician evaluation post-triage.")
with cf3:
    with st.container(border=True):
        st.markdown("#### 🏥 Hospital Status")
        st.markdown("Predicts general facility crowding categories (Functional, Overcrowded, Overwhelmed).")
    with st.container(border=True):
        st.markdown("#### 📈 Admission Likelihood")
        st.markdown("Evaluates multi-variable indicators to gauge clinical inpatient bed requirements.")

st.write("")

# --- 6️⃣ TECHNOLOGY PREVIEW ---
st.markdown("### 💻 Built Using")
with st.container(border=True):
    st.markdown("""
    <span class="tech-badge">Python</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Scikit-Learn</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">Joblib</span>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("---")

# --- 7️⃣ FOOTER ---
st.caption("Developed as an AI-powered Emergency Department Decision Support System using Machine Learning and FastAPI.")