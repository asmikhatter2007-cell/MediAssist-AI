import streamlit as st

st.set_page_config(
    page_title="After Triage",
    page_icon="🚑",
    layout="wide"
)

st.title("🚑 After Triage")
st.caption("Clinical Decision Support after Triage Assessment")

st.divider()

st.subheader("Patient Information")

col1, col2 = st.columns(2)

with col1:
    age = st.slider(
        "Age",
        min_value=0,
        max_value=100,
        value=30
    )

    sex = st.selectbox(
        "Sex",
        [
            "male",
            "female"
        ]
    )

with col2:

    arrival_options = {
    "Private Vehicle": "private_vehicle",
    "Walk-in": "walk_in",
    "Ambulance": "ambulance",
    "Referred": "referred",
    "Police": "police"
    }

    selected = st.selectbox(
        "Arrival Mode",
        list(arrival_options.keys())
    )

    arrival_mode = arrival_options[selected]

    chronic_illness = st.selectbox(
        "Chronic Illness",
        [
            "No",
            "Yes"
        ]
    )

st.divider()

st.subheader("Triage Information")

col3, col4 = st.columns(2)

with col3:

    triage_category = st.selectbox(
        "Triage Category",
        [
            "non_urgent",
            "standard",
            "urgent",
            "very_urgent",
            "emergency"
        ]
    )

with col4:

    chief_complaint = st.selectbox(
        "Chief Complaint",
        [
            "abdominal_pain",
            "cardiovascular",
            "fever_infection",
            "neurological",
            "obstetric_gynae",
            "other",
            "poisoning",
            "respiratory",
            "surgical",
            "trauma"
        ]
    )

st.divider()

predict = st.button(
    "Predict",
    type="primary",
    use_container_width=True
)

st.divider()

st.subheader("Prediction Results")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        label="🏥 Hospital Status",
        value="Waiting..."
    )

with c2:
    st.metric(
        label="👨‍⚕️ Doctor Wait Time",
        value="-- min"
    )

with c3:
    st.metric(
        label="📋 Admission Probability",
        value="-- %"
    )

st.info(
    "Admission Prediction and Doctor Wait Time will be connected once the APIs are integrated."
)