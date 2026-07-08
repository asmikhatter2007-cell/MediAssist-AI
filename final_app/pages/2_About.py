"""
MODEL 1 - ABOUT PAGE
=============================================================
Informational page: full project architecture, models, dataset,
and team credits - correctly scoped as a group project.
"""

import streamlit as st

st.set_page_config(page_title="About - MediAssist AI", page_icon="📋", layout="centered")

st.title("📋 About This Project")

st.markdown(
    """
    ### Project Overview
    **MediAssist AI** is a group project built around a two-stage patient
    journey: helping patients decide whether and where to seek care
    *before* arriving at a hospital, and helping hospitals manage patient
    flow and predict outcomes *after* a patient has been triaged.
    """
)

st.divider()

st.markdown("### 🗺️ System Architecture")

st.markdown("**Stage 1 — Before Triage** *(\"Should I go, and where?\")*")
st.markdown(
    """
    - **Symptom → Department/Condition prediction** — patient-facing symptom
      checker with confidence scores and SHAP explainability
    - **Hospital overcrowding status** — real-time hospital load indicator
    - **Predicted triage wait time** — estimated wait before being seen
    """
)

st.markdown("**Stage 2 — After Triage** *(\"I'm here, what now?\")*")
st.markdown(
    """
    - **Hospital overcrowding status** — same model, refreshed with current data
    - **Predicted doctor wait time** — using the patient's real triage category
    - **Admission likelihood** — probability of hospital admission
    - **Length of stay prediction** — estimated duration of hospital stay
    """
)

st.divider()

st.markdown("### 🤖 This Component: Symptom → Department/Condition")
st.write(
    "This app demonstrates the Stage 1 symptom-prediction component. It "
    "predicts the most likely condition from reported symptoms, along with "
    "a confidence score and recommended specialist/department."
)

st.markdown("**Model selection**")
st.write(
    "Logistic Regression, Random Forest, and XGBoost were compared using "
    "accuracy, precision, recall, and F1 score. Logistic Regression was "
    "selected as the final model, with an additional deduplicated "
    "evaluation performed to check for data leakage."
)

st.markdown("**Explainability (SHAP)**")
st.write(
    "Every prediction is accompanied by a SHAP-based explanation showing "
    "which symptoms contributed most to the result, and in which direction "
    "(supporting or contradicting the predicted condition)."
)

st.markdown("**Dataset used for this component**")
st.write(
    "Disease-Symptom dataset (Kaggle): 4,920 patient records covering "
    "41 conditions and 131 unique symptoms."
)
st.caption(
    "Source: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset"
)

st.divider()

st.markdown("### 🛠️ Tech Stack")
st.markdown(
    """
    - **Python** — core language
    - **Scikit-learn** — model training & evaluation
    - **SHAP** — explainable AI
    - **FastAPI** — backend API
    - **Streamlit** — frontend web app
    - **Plotly** — data visualization
    """
)

st.divider()

st.markdown("### 👥 Team")
st.write(
    "Built by a team of three as part of an internship project, with each "
    "member responsible for a distinct stage of the system: symptom-based "
    "prediction and triage routing, hospital overcrowding and wait-time "
    "modeling, and post-triage admission/length-of-stay prediction."
)

st.caption(
    "⚠️ This tool is for educational/informational purposes only and is not "
    "a substitute for professional medical advice."
)