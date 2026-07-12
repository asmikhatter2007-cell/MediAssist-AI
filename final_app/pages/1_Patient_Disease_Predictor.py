import streamlit as st
import requests
import plotly.graph_objects as go
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

# Page config
st.set_page_config(
    page_title="Patient Disease Predictor", 
    page_icon="🧬", 
    layout="wide"
)
render_sidebar(1)

# Global Premium Theme Injector
st.markdown("""
<style>
header[data-testid="stHeader"]{ background: #0C1024 !important; }
[data-testid="stToolbar"]{ background: transparent !important; }
html, body{ background: #0C1024 !important; }
.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        radial-gradient(circle at 20% 92%, rgba(244,114,182,0.10), transparent 45%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

/* FIX: Split title styling so the emoji doesn't get masked as a solid square */
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
}

/* Multiselect Styling Box */
div[data-baseweb="select"] > div{
    background: rgba(255,255,255,0.06) !important;
    border:1.5px solid rgba(129,140,248,0.45) !important;
    border-radius:12px !important;
}

/* SUPER EXPLICIT FIX: Force the gray placeholder text inside the multi-select input to be crisp white */
div[data-baseweb="select"] input::placeholder,
div[data-baseweb="select"] [data-baseweb="select"] div,
div[data-baseweb="select"] div {
    color: #ffffff !important;
}

/* ================= MATCHED BUTTON OVERRIDES ================= */
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
</style>
""", unsafe_allow_html=True)

# Re-rendered title block separating the emoji icon from the gradient text text-fill masking properties
st.markdown("""
<div class="title-container">
    <span class="title-icon">🧬</span>
    <span class="title-text">Patient Disease Predictor</span>
</div>
""", unsafe_allow_html=True)
st.caption("Clinical Decision Support Tool & Predictive Diagnosis Assessment")

BASE_URL = "http://127.0.0.1:8000"

# Fetch the valid symptom list from the backend instead of loading the model locally
@st.cache_data
def load_symptom_options():
    response = requests.get(f"{BASE_URL}/valid_symptoms")
    response.raise_for_status()
    return response.json()["symptoms"]

try:
    symptom_options = load_symptom_options()
except Exception:
    symptom_options = []
    st.error("Backend is not running.")

with st.container(border=True):
    st.subheader("📋 Patient Symptoms")
    selected_symptoms = st.multiselect(
        "Select your symptoms",
        options=symptom_options,
        placeholder="Start typing a symptom...",
        label_visibility="collapsed"
    )

st.write("")
# FIXED: Added use_container_width=True here to stretch across the UI cards
predict_clicked = st.button("Predict", type="primary", disabled=len(selected_symptoms) == 0, use_container_width=True)

if predict_clicked:
    try:
        response = requests.post(
            f"{BASE_URL}/predict_disease",
            json={"symptoms": selected_symptoms, "top_n": 3}
        )
        response.raise_for_status()
        result = response.json()
    except Exception:
        result = {"error": "Backend is not running or returned an error."}

    if "error" in result:
        st.error(result["error"])
    else:
        top = result["top_predictions"][0]

        with st.container(border=True):
            st.subheader(f"Predicted Disease: {top['disease']}")
            st.metric("Confidence", f"{top['confidence']}%")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Recommended Specialist:**  \n`{top['specialist']}`")
            with col2:
                st.markdown(f"**Hospital Department:**  \n`{top['department']}`")

            st.markdown("---")
            st.markdown(f"**Description:**  \n{result['description']}")

            st.markdown("---")
            st.markdown("**Precautions:**")
            for p in result["precautions"]:
                st.markdown(f"• {p.capitalize()}")

        if len(result["top_predictions"]) > 1:
            with st.container(border=True):
                st.subheader("Other Possibilities Considered")
                for pred in result["top_predictions"][1:]:
                    st.markdown(f"• **{pred['disease']}** ({pred['confidence']}% confidence) → *{pred['specialist']}*")

        with st.container(border=True):
            st.subheader("💡 Why was this predicted?")
            
            shap_data = result["shap_explanation"]
            symptoms_list = [item["symptom"] for item in shap_data][::-1]
            contributions = [item["contribution"] for item in shap_data][::-1]
            colors = ["#2DD4BF" if c >= 0 else "#F472B6" for c in contributions]

            fig = go.Figure(go.Bar(
                x=contributions,
                y=symptoms_list,
                orientation="h",
                marker_color=colors,
                text=[f"{c:+.3f}" for c in contributions],
                textposition="outside",
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#EEF1FB'),
                xaxis=dict(title="Contribution to prediction", gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("🟢 Green items pushed toward this diagnosis. 🔴 Pink items pushed away from it.")