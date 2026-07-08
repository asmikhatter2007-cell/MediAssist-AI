import streamlit as st

st.set_page_config(page_title="Before Triage", page_icon="🩺")

st.title("🩺 Before Triage")
st.caption("AI Assistance before arriving at the Emergency Department")

st.divider()

st.subheader("Step 1 • Select Symptoms")

symptoms = st.multiselect(
    "Choose your symptoms",
    [
        "Fever",
        "Cough",
        "Headache",
        "Chest Pain",
        "Vomiting",
        "Fatigue",
        "Shortness of Breath"
    ]
)

st.button("Predict Disease", type="primary")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Disease Prediction")

    st.metric(
        "Predicted Disease",
        "Waiting..."
    )

    st.metric(
        "Confidence",
        "-- %"
    )

with col2:
    st.subheader("Recommended Department")

    st.info("General Medicine")

st.divider()

st.subheader("Hospital Status")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Overcrowding",
        "Normal"
    )

with c2:
    st.metric(
        "Estimated Triage Wait",
        "-- mins"
    )