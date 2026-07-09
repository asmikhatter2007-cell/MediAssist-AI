import streamlit as st
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar(3) # Index 3 for Dashboard

st.title("📊 Emergency Department Dashboard")

st.caption("Hospital Analytics")

st.divider()

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Patients Today",
        "248"
    )

with c2:
    st.metric(
        "Average Wait",
        "34 min"
    )

with c3:
    st.metric(
        "Admissions",
        "72"
    )

with c4:
    st.metric(
        "Beds Available",
        "15"
    )

st.divider()

st.subheader("Hospital Status")

st.success("🟢 Normal")

st.divider()

st.subheader("Analytics")

st.info("Interactive graphs will appear here after integration.")