import streamlit as st
from navigation import render_sidebar

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🏥",
    layout="wide",
)
# Render the sidebar for Home (Index 0)
render_sidebar(0)

# ---------------- HERO SECTION----------------
# The rest of your code runs normally only when "🏠 Home" is selected
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