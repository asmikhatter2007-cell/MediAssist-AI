import streamlit as st
import sys
import os

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar(3)

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

# Main Metrics Row - Rebuilt to eliminate native gray wrapping constraints
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="metric-header">👥 Patients Today</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">248</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-header">🕒 Average Wait</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">34 min</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-header">📋 Admissions</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">72</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="metric-header">🛏️ Beds Available</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">15</div>', unsafe_allow_html=True)

st.write("")

# Analytics Lists Wrapped in Glass containers
with st.container(border=True):
    st.subheader("📈 Operational Analytics Modules")
    
    modules = [
        ("📈 Wait Time Trend", "Real-time historical graph tracks localized emergency bottlenecks."),
        ("📊 Peak Activity Hours", "Hourly distribution analysis shows highest arrival windows."),
        ("📅 Weekly Busy Cycles", "Aggregated workflow data highlights resource strain spikes."),
        ("🚑 Chief Complaint Footprint", "Dynamic breakdown displays primary clinical categories.")
    ]
    
    for title, desc in modules:
        st.markdown(f"""
        <div class="analytic-item">
            <div><strong>{title}</strong> — <span style="color:#9BA3C7;">{desc}</span></div>
        </div>
        """, unsafe_allow_html=True)