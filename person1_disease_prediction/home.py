"""
MODEL 1 - HOME PAGE (main entry point)
=============================================================
This becomes the app's landing page. Streamlit automatically turns any
.py file inside a pages/ folder into an additional page with sidebar
navigation - no routing code needed.

Run with:
    streamlit run Home.py
"""

import streamlit as st

st.set_page_config(
    page_title="MediAssist AI - Home",
    page_icon="🏥",
    layout="centered",
)

st.title("🏥 MediAssist AI")
st.subheader("An Explainable AI-Based Hospital Decision Support System")

st.write(
    "This is a group project built around a two-stage patient journey — "
    "helping patients decide whether and where to go, and helping hospitals "
    "manage flow once they arrive."
)

st.divider()

st.markdown("### 🗺️ Project Architecture")

st.markdown("**Stage 1 — Before Triage** *(\"Should I go, and where?\")*")
st.markdown(
    """
    - 🩺 Symptom → Department/Condition prediction *(this component — see Patient Assistant)*
    - 🏨 Hospital overcrowding status
    - ⏱️ Predicted triage wait time
    """
)

st.markdown("**Stage 2 — After Triage** *(\"I'm here, what now?\")*")
st.markdown(
    """
    - 🏨 Hospital overcrowding status *(same model, refreshed)*
    - ⏱️ Predicted doctor wait time *(using the real triage category)*
    - 📥 Admission likelihood
    - 🛏️ Length of stay prediction
    """
)

st.caption(
    "This app currently demonstrates the **Symptom → Department/Condition** "
    "component of Stage 1. The remaining components are separate models "
    "built by teammates as part of the same overall system."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🩺 Try It: Patient Assistant")
    st.write(
        "Select your symptoms and get an instant prediction of the most "
        "likely condition, how confident the model is, which specialist to "
        "see, and a clear explanation of *why* that prediction was made."
    )
    st.info("👈 Use the sidebar to open **Patient Assistant**")

with col2:
    st.markdown("### 📋 About This Project")
    st.write(
        "Learn about the full project architecture, the models involved, "
        "the datasets used, and the team behind each component."
    )
    st.info("👈 Use the sidebar to open **About**")

st.divider()

st.markdown("### How this component works")
st.markdown(
    """
    1. **Select your symptoms** from a checklist (no need to know medical terms)
    2. **Get a prediction** — the top 3 most likely conditions, ranked by confidence
    3. **See the recommended specialist and hospital department**
    4. **Understand why** — a SHAP-based explanation shows exactly which
       symptoms drove the prediction, and by how much
    """
)

st.caption(
    "⚠️ This tool is for educational/informational purposes only and is not "
    "a substitute for professional medical advice. Always consult a doctor."
)