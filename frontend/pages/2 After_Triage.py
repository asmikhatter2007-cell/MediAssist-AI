import streamlit as st

st.set_page_config(page_title="After Triage", page_icon="🚑")

st.title("🚑 After Triage")
st.caption("Decision Support after hospital triage")

st.divider()

col1, col2 = st.columns(2)

with col1:

    age = st.number_input("Age", 1, 120)

    gender = st.selectbox(
        "Gender",
        ["Male","Female"]
    )

    arrival = st.selectbox(
        "Arrival Mode",
        ["Walk-in","Ambulance"]
    )

with col2:

    complaint = st.text_input("Chief Complaint")

    triage = st.selectbox(
        "Triage Category",
        ["Red","Orange","Yellow","Green"]
    )

st.button("Predict", type="primary")

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Hospital Status",
        "Normal"
    )

with c2:
    st.metric(
        "Doctor Wait",
        "-- mins"
    )

with c3:
    st.metric(
        "Admission Chance",
        "-- %"
    )

st.info("Admission Prediction model will be connected next.")