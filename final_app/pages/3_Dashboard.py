import streamlit as st
import random
import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar(3)

TOTAL_BEDS=30

# -------------------------------
# Temporary Dashboard Data
# -------------------------------

if "dashboard_data" not in st.session_state:

    st.session_state.dashboard_data = {
        "patients_today": random.randint(180, 320),
        "average_wait": random.randint(20, 55),
        "admissions": random.randint(40, 90),
        "beds_available": random.randint(5, 25),
        "last_updated": datetime.now().strftime("%d %b %Y • %I:%M %p")
    }
# Theme Styles Injector
st.markdown("""
<style>
header[data-testid="stHeader"]{ background: #0C1024 !important; }
html, body{ background: #0C1024 !important; }
.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

/* Dashboard Emoji Layout fix container rules */
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

h2, h3 { color:#EDEFFC !important; font-weight:700 !important; }
div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius:22px !important;
    border:1px solid rgba(255,255,255,0.09) !important;
    padding:20px !important;
}
.status-pill { padding: 10px 20px; border-radius: 12px; font-weight: 700; display: inline-block; margin-bottom: 15px; }
.status-busy { background: rgba(251,191,110,0.15); color: #FBBF6E; border: 1px solid rgba(251,191,110,0.3); }
.analytic-item { background: rgba(255,255,255,0.03); padding: 16px; border-radius: 14px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.06); display: flex; align-items: center; gap: 12px; }
.metric-header { font-size: 14.5px; font-weight: 600; color: #9BA3C7; margin-bottom: 2px; }
.metric-value { font-size: 34px; font-weight: 800; color: #2DD4BF; margin-top: 0px; }
</style>
""", unsafe_allow_html=True)

# Custom aligned title layout block 
st.markdown("""
<div class="title-container">
    <span class="title-icon">📊</span>
    <span class="title-text">Emergency Department Dashboard</span>
</div>
""", unsafe_allow_html=True)
st.caption("Real-Time Hospital Resource Analytics")

# Custom Status Indicator Row
st.markdown('<div class="status-pill status-busy">🟠 System Status: Busy</div>', unsafe_allow_html=True)

st.caption(
    f"🕒 Last Updated: {st.session_state.dashboard_data['last_updated']}"
)

# Main Metrics Row - Rebuilt to eliminate native gray wrapping constraints
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="metric-header">👥 Patients Today</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{st.session_state.dashboard_data["patients_today"]}</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-header">🕒 Average Wait</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{st.session_state.dashboard_data["average_wait"]} min</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-header">📋 Admissions</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{st.session_state.dashboard_data["admissions"]}</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="metric-header">🛏️ Beds Available</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{st.session_state.dashboard_data["beds_available"]}</div>', unsafe_allow_html=True)

st.write("")

# Analytics Lists Wrapped in Glass containers
with st.container(border=True):

    st.subheader("📈 Department Analytics")

    col1, col2 = st.columns(2)

    with col1:

        hours = [f"{i}:00" for i in range(8, 21)]

        waits = [
            max(
                10,
                st.session_state.dashboard_data["average_wait"] + random.randint(-8, 8)
            )
            for _ in hours
        ]

        df = pd.DataFrame({"Hour": hours, "Wait": waits})

        fig = px.line(df, x="Hour", y="Wait", markers=True)
        fig.update_traces(line_color="#2DD4BF", marker=dict(color="#F472B6", size=7))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="Wait Time Trend",
            height=350,
            font=dict(color="#EEF1FB")
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)

    with col2:

        df = pd.DataFrame({
            "Complaint": ["Respiratory", "Trauma", "Cardiac", "Fever", "Abdominal"],
            "Patients": [
                random.randint(20, 45),
                random.randint(15, 40),
                random.randint(10, 25),
                random.randint(12, 30),
                random.randint(10, 28)
            ]
        })

        fig = px.bar(df, x="Complaint", y="Patients", color="Patients",
                     color_continuous_scale=["#818CF8", "#2DD4BF"])
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title="Chief Complaints",
            height=350,
            font=dict(color="#EEF1FB"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)


with st.container(border=True):

    st.subheader("🛏 Bed Occupancy")

    beds_available = st.session_state.dashboard_data["beds_available"]
    occupied_pct = ((TOTAL_BEDS - beds_available) / TOTAL_BEDS) * 100
    occupied_pct = min(max(occupied_pct, 0), 100)

    gcol1, gcol2, gcol3 = st.columns([1, 2, 1])  # center it, cap its width

    with gcol2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=occupied_pct,
            number={"suffix": "%", "font": {"size": 36}},
            title={"text": "Occupied Beds", "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2DD4BF"},
                "bgcolor": "rgba(255,255,255,0.04)",
                "steps": [
                    {"range": [0, 50], "color": "#2A3452"},
                    {"range": [50, 75], "color": "#3D4A73"},
                    {"range": [75, 100], "color": "#F472B6"}
                ],
                "threshold": {
                    "line": {"color": "#F472B6", "width": 4},
                    "thickness": 0.8,
                    "value": occupied_pct
                }
            }
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(color="white")
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)