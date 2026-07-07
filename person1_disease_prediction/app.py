"""
MODEL 1 - PATIENT ASSISTANT WEB APP (Streamlit)
=============================================================
Page 1 from your spec doc: Symptoms -> Disease Prediction -> Confidence
-> Department -> Description -> Precautions -> SHAP Explanation

Run with:
    streamlit run app.py

Must be in the same folder as:
    inference_pipeline_final.py
    models/ (disease_prediction_model.pkl, label_encoder.pkl, feature_columns.pkl)
    data/processed/ (description_clean.csv, precaution_clean.csv, multihot_symptom_matrix.csv)
    disease_specialist_department_final.csv
"""

import streamlit as st
import plotly.graph_objects as go
from inference_pipeline_final import DiseasePredictor

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Disease Prediction Assistant", page_icon="🏥", layout="centered")


# ---------------------------------------------------------------------------
# Load the predictor once and cache it (avoids reloading the model on every
# click/interaction - Streamlit reruns the whole script top-to-bottom
# every time a widget changes)
# ---------------------------------------------------------------------------
@st.cache_resource
def load_predictor():
    return DiseasePredictor()


predictor = load_predictor()
symptom_options = predictor.get_symptom_list()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🏥 Patient Assistant")
st.caption("Select your symptoms below to get a disease prediction, "
           "recommended specialist, and explanation.")

# ---------------------------------------------------------------------------
# Symptom input
# ---------------------------------------------------------------------------
selected_symptoms = st.multiselect(
    "Select your symptoms",
    options=symptom_options,
    placeholder="Start typing a symptom...",
)

predict_clicked = st.button("Predict", type="primary", disabled=len(selected_symptoms) == 0)

# ---------------------------------------------------------------------------
# Prediction + results
# ---------------------------------------------------------------------------
if predict_clicked:
    result = predictor.predict(selected_symptoms)

    if "error" in result:
        st.error(result["error"])
    else:
        top = result["top_predictions"][0]

        st.divider()

        # --- Main prediction ---
        st.subheader(f"Predicted Disease: {top['disease']}")
        st.metric("Confidence", f"{top['confidence']}%")

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Recommended Specialist**")
            st.write(top["specialist"])
        with col2:
            st.write("**Hospital Department**")
            st.write(top["department"])

        # --- Description ---
        st.write("**Description**")
        st.write(result["description"])

        # --- Precautions ---
        st.write("**Precautions**")
        for p in result["precautions"]:
            st.write(f"- {p.capitalize()}")

        # --- Other candidate diseases (top 2 and 3) ---
        if len(result["top_predictions"]) > 1:
            st.divider()
            st.write("**Other possibilities considered:**")
            for pred in result["top_predictions"][1:]:
                st.write(f"- {pred['disease']} ({pred['confidence']}% confidence) "
                         f"-> {pred['specialist']}")

        # --- SHAP explanation ---
        st.divider()
        st.subheader("Why was this predicted?")

        shap_data = result["shap_explanation"]
        symptoms_list = [item["symptom"] for item in shap_data][::-1]
        contributions = [item["contribution"] for item in shap_data][::-1]
        colors = ["#2ecc71" if c >= 0 else "#e74c3c" for c in contributions]

        fig = go.Figure(go.Bar(
            x=contributions,
            y=symptoms_list,
            orientation="h",
            marker_color=colors,
            text=[f"{c:+.3f}" for c in contributions],
            textposition="outside",
        ))
        fig.update_layout(
            xaxis_title="Contribution to prediction",
            yaxis_title="",
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption("Green = pushed toward this diagnosis. Red = pushed away from it.")

        if result["unknown_symptoms"]:
            st.warning(f"Note: these entries weren't recognized and were ignored: "
                       f"{result['unknown_symptoms']}")