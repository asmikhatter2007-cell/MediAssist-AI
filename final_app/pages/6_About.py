import streamlit as st
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(
    page_title="MediAssist AI - About", 
    page_icon="📋", 
    layout="wide"
)
render_sidebar(6) 

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
    font-weight:800 !important;
    font-size:2.5rem !important;
}
h2, h3, h4 { color:#EDEFFC !important; font-weight:700 !important; margin-top:10px;}

div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:24px !important;
    margin-bottom: 20px;
}
div[data-testid="stVerticalBlockBorderWrapper"] p { color: #EEF1FB !important; font-size: 15px !important; }
li { color: #C3CAE8 !important; margin-bottom: 8px; font-size: 14.5px !important; }

/* Custom table layout styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 14.5px;
}
th {
    background: rgba(129,140,248,0.15);
    color: #2DD4BF !important;
    text-align: left;
    padding: 12px;
    font-weight: 700;
    border-bottom: 2px solid rgba(255,255,255,0.1);
}
td {
    padding: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #EEF1FB;
}
</style>
""", unsafe_allow_html=True)

# --- 1️⃣ HERO BANNER ---
st.markdown("""
<div class="title-container">
    <span class="title-icon">📋</span>
    <span class="title-text">About MediAssist AI</span>
</div>
""", unsafe_allow_html=True)
st.caption("Understanding the System Architecture and Machine Learning Pipeline")

# --- 2️⃣ PROJECT OVERVIEW ---
with st.container(border=True):
    st.subheader("🏥 Project Overview")
    st.markdown(
        "MediAssist AI is a machine learning–based Emergency Department Decision Support System developed to improve patient guidance and optimize hospital operations. "
        "The platform combines multiple predictive models into a unified workflow that assists patients before and after triage while providing hospital administrators with live operational insights."
    )

# --- 3️⃣ PROJECT OBJECTIVES ---
st.markdown("### 🎯 Objectives")
ob1, ob2, ob3, ob4 = st.columns(4)
with ob1:
    with st.container(border=True):
        st.markdown("#### 🧑‍⚕️ Patient Experience")
        st.markdown("<p style='font-size:13.5px; color:#C3CAE8;'>Reduce uncertainty by providing real-time healthcare journey guidance.</p>", unsafe_allow_html=True)
with ob2:
    with st.container(border=True):
        st.markdown("#### 🏥 Hospital Efficiency")
        st.markdown("<p style='font-size:13.5px; color:#C3CAE8;'>Monitor hospital resources and predict active operational load boundaries.</p>", unsafe_allow_html=True)
with ob3:
    with st.container(border=True):
        st.markdown("#### 🤖 AI Decision Support")
        st.markdown("<p style='font-size:13.5px; color:#C3CAE8;'>Provide intelligent predictions using trained machine learning models.</p>", unsafe_allow_html=True)
with ob4:
    with st.container(border=True):
        st.markdown("#### 📈 Resource Analytics")
        st.markdown("<p style='font-size:13.5px; color:#C3CAE8;'>Assist medical administrators in strategic resource planning.</p>", unsafe_allow_html=True)

st.write("")

# --- 4️⃣ SYSTEM ARCHITECTURE ---
with st.container(border=True):
    st.subheader("⚙️ System Workflow Architecture")
    st.markdown(
        """
        <p style='text-align: center; font-size: 15px; color: #2DD4BF; font-weight: 600;'>
        Patient Input ➜ Symptom Checker ➜ Disease Prediction ➜ Before Triage Assistant ➜ Hospital Visit ➜ Triage Assessment ➜ After Triage Assistant ➜ Hospital Dashboard
        </p>
        """, unsafe_allow_html=True
    )

st.write("")

# --- 5️⃣ MACHINE LEARNING MODELS ---
with st.container(border=True):
    st.subheader("🤖 Machine Learning Models Pipeline")
    st.markdown(
        """
        <table>
            <tr>
                <th>Model</th>
                <th>Target Purpose</th>
            </tr>
            <tr>
                <td><b>Disease Prediction Model</b></td>
                <td>Predicts the most probable disease class based on custom symptom checks.</td>
            </tr>
            <tr>
                <td><b>Hospital Status Model</b></td>
                <td>Classifies real-time congestion state into Functional, Overcrowded, or Overwhelmed.</td>
            </tr>
            <tr>
                <td><b>Wait Time Prediction Model</b></td>
                <td>Estimates registration desk check-in delay bounds prior to clinical entry.</td>
            </tr>
            <tr>
                <td><b>Doctor Wait Prediction Model</b></td>
                <td>Predicts processing duration remaining until private physician bedside examination.</td>
            </tr>
            <tr>
                <td><b>Admission Likelihood Model</b></td>
                <td>Estimates the point-based probability that a patient will require an inpatient room assignment.</td>
            </tr>
        </table>
        """, unsafe_allow_html=True
    )

st.write("")

# --- 6️⃣ TECHNOLOGY STACK & 7️⃣ DATASETS ---
col_t1, col_t2 = st.columns(2)
with col_t1:
    with st.container(border=True):
        st.subheader("🛠 Technology Stack")
        st.markdown("""
        * **Backend Framework:** Python • FastAPI terminal routers
        * **Frontend Container:** Streamlit web engine components
        * **Machine Learning:** Scikit-Learn • Random Forest • Gradient Boosting
        * **Data Processing:** Pandas • NumPy • Joblib model compression
        """)
with col_t2:
    with st.container(border=True):
        st.subheader("📊 Datasets Used")
        st.markdown("""
        * 🩺 **Disease Dataset** — Symptom matrix arrays for diagnostic maps
        * 🏥 **Hospital Resource Dataset** — Logistics telemetry indicators for status tracking
        * ⏳ **Emergency Department Dataset** — Time stamp records for registration forecasting
        * 📈 **Patient Flow Dataset** — Vulnerability indicator fields for likelihood checks
        """)

st.write("")

# --- 8️⃣ KEY FUNCTIONALITIES ---
with st.container(border=True):
    st.subheader("🌟 System Capabilities")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.markdown("#### Patient Module Features")
        st.markdown("""
        * Real-time automated illness diagnostics mapping
        * Clinic specialist tracking assignment recommendations
        * End-to-end timing indicators before formal triage registration
        * Personalized physician examination waiting predictions
        * Automated data syncing based on session parameters
        """)
    with f_col2:
        st.markdown("#### Hospital Module Features")
        st.markdown("""
        * Dynamic admin data panel logs for resource parameters
        * Real-time machine learning infrastructure load classification
        * Instant staff ratio metrics updating (Doctors / Nurses)
        * Active tracking indicators for occupied beds and test queues
        * Multi-client infrastructure layout streaming
        """)

st.write("")

# --- 9️⃣ DISCLAIMER ---
with st.container(border=True):
    st.markdown("<h4 style='color:#F87171 !important;'>⚠️ Disclaimer Context</h4>", unsafe_allow_html=True)
    st.caption("MediAssist AI is developed for educational and decision-support purposes only. It is not intended to replace professional medical diagnosis, emergency triage, or clinical judgment. Final medical decisions should always be made by qualified healthcare professionals.")