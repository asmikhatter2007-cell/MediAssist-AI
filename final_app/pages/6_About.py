import streamlit as st
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="About - MediAssist AI", page_icon="📋", layout="wide")
render_sidebar(6) 

# Inject global style wrappers
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

/* FIX: Splits up the header array to isolate document emoji layouts from text backgrounds */
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
</style>
""", unsafe_allow_html=True)

# Fixed Custom Title Layout
st.markdown("""
<div class="title-container">
    <span class="title-icon">📋</span>
    <span class="title-text">About This Project</span>
</div>
""", unsafe_allow_html=True)
st.caption("System Architecture and Core Methodologies")

with st.container(border=True):
    st.subheader("Project Overview")
    st.markdown(
        "**MediAssist AI** is a collaborative group project built around an optimized two-stage patient journey: "
        "helping individuals evaluate conditions *before* reaching a healthcare center, and assisting administrative "
        "teams to triage flow and predict occupancy demands *after* patient check-in."
    )

with st.container(border=True):
    st.subheader("🗺️ System Architecture Roadmap")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Stage 1 — Before Triage")
        st.markdown(
            """
            - **Symptom Tracker Module** — Classifies conditions using confidence weights and SHAP explanations.
            - **Live Overcrowding Index** — Displays immediate clinical workload metrics.
            - **Estimated Waiting Forecast** — Computes wait time window before patient processing.
            """
        )
    with col2:
        st.markdown("#### Stage 2 — After Triage")
        st.markdown(
            """
            - **Refreshed Status Matrix** — Syncs current workflow demands to backend counters.
            - **Doctor Wait Predictor** — Evaluates physician availability by specific triage category.
            - **Admission Likelihood Engine** — Computes probability vectors for hospital admission.
            """
        )

with st.container(border=True):
    st.subheader("🤖 Technical Execution Stack")
    st.markdown(
        """
        - **Core Architecture:** Logistic Regression models evaluated against Random Forest and XGBoost arrays.
        - **Explainability Frame:** SHAP-based horizontal direction arrays map exact clinical feature tracking weights.
        - **Dataset Metrics:** Disease-Symptom database compiling 4,920 profile records across 41 health classifications.
        - **Development Engine:** Python, Scikit-Learn, SHAP, FastAPI, Streamlit, and Plotly graphics.
        """
    )
    st.caption("⚠️ Educational Resource Tool: Built for clinical workflow simulation purposes and is not a substitute for direct professional diagnostics.")