import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🏥",
    layout="wide",
)

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
        width=80
    )

    st.title("MediAssist AI")

    st.markdown("---")

    st.markdown("### Navigation")

    st.write("🏠 Home")
    st.write("🩺 Before Triage")
    st.write("🚑 After Triage")
    st.write("📊 Dashboard")

    st.markdown("---")

    st.info(
        "Select a module from the Pages section below."
    )

# ---------------- HERO SECTION ----------------
st.markdown("""
<h1 style='text-align:center; color:#0E4C92; font-size:52px;'>
🏥 MediAssist AI
</h1>

<h3 style='text-align:center; color:#4F4F4F;'>
AI-Powered Emergency Department Decision Support System
</h3>

<p style='text-align:center; font-size:18px; color:#666666;'>
Helping patients make smarter emergency decisions before and after triage.
</p>
""", unsafe_allow_html=True)

st.write("")

# ---------------- INTRO ----------------
st.markdown("""
### Welcome

MediAssist AI is an intelligent healthcare support platform that assists
patients during emergency visits by predicting:

- 🩺 Disease / Department Recommendation
- 🏥 Hospital Overcrowding Status
- ⏳ Estimated Waiting Time
- 🚑 Admission Probability
""")

st.write("")

col1, col2 = st.columns(2)

with col1:
    st.info("""
### 🩺 Stage 1 — Before Triage

This stage helps patients decide:

✅ Which department to visit

✅ Hospital crowd level

✅ Estimated triage waiting time
""")

with col2:
    st.success("""
### 🚑 Stage 2 — After Triage

Once triage is completed:

✅ Updated hospital status

✅ Doctor waiting time

✅ Admission likelihood
""")
    
st.write("")

st.markdown("---")

st.caption(
    "Developed as an AI-powered Emergency Department Decision Support System using Machine Learning, FastAPI and Streamlit."
)

st.write("")
