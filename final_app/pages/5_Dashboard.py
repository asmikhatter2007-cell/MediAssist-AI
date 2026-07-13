import streamlit as st
import requests
import sys
import os
import pandas as pd
import plotly.express as px

# Navigation Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
render_sidebar(5)

BASE_URL = "https://mediassist-ai-68lg.onrender.com"

# CHANGE THIS before submission / demo - different from Admin's password
STAFF_PASSWORD = "staff123"

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

.title-container { display: flex; align-items: center; gap: 15px; margin-bottom: 5px; }
.title-icon { font-size: 2.8rem; }
.title-text {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
}

h2, h3 { color:#EDEFFC !important; font-weight:700 !important; }
div[class*="st-key-card_"]{
    background: rgba(255,255,255,0.07) !important;
    border-radius:20px !important;
    border:1.5px solid rgba(129,140,248,0.35) !important;
    box-shadow: 0 12px 32px rgba(0,0,0,0.4) !important;
    padding:20px !important;
}
.status-pill { padding: 10px 20px; border-radius: 12px; font-weight: 700; display: inline-block; margin-bottom: 15px; }
.status-functional { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
.status-busy { background: rgba(251,191,110,0.15); color: #FBBF6E; border: 1px solid rgba(251,191,110,0.3); }
.status-overwhelmed { background: rgba(248,113,113,0.15); color: #F87171; border: 1px solid rgba(248,113,113,0.3); }

.metric-card { display:flex; align-items:center; gap:14px; padding:16px 18px; }
.metric-icon { width:44px; height:44px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:19px; flex-shrink:0; }
.metric-header { font-size: 13px; font-weight: 600; color: #9BA3C7; margin-bottom: 3px; }
.metric-value { font-size: 26px; font-weight: 800; color: #EEF1FB; }

/* --- UPDATED: Full-Width Gradient Buttons with Extra Bold Font Targets --- */
.stButton>button{
    width:100% !important; border-radius:16px !important; height:58px !important;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%) !important;
    background-size: 200% auto !important; color:#0C1024 !important; font-size:19px !important; font-weight:800 !important; border:none !important;
    box-shadow: 0 14px 34px rgba(129,140,248,0.30) !important; transition: all 0.25s ease !important;
}
.stButton>button:hover{ background-position: right center !important; transform: translateY(-2px) !important; }
.stButton>button p, .stButton>button span div, .stButton>button div p { color:#0C1024 !important; font-weight:800 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <span class="title-icon">📊</span>
    <span class="title-text">Emergency Department Dashboard</span>
</div>
""", unsafe_allow_html=True)
st.caption("Real-Time Hospital Resource Analytics")

# ---------------- LOGIN GATE ----------------
if "staff_authenticated" not in st.session_state:
    st.session_state.staff_authenticated = False

if not st.session_state.staff_authenticated:
    with st.container(border=True):
        st.subheader("🔑 Staff Login")
        password_input = st.text_input("Password", type="password")
        

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. Create columns to center the button nicely inside the card
        _, btn_col, _ = st.columns([1.5, 1, 1.5])
        
        with btn_col:
            # 2. Place the button inside the middle column
            if st.button("Login", type="primary", use_container_width=True):
                if password_input == STAFF_PASSWORD:
                    st.session_state.staff_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
    st.stop()

col_a, col_b = st.columns([5, 1])
with col_a:
    st.success("Logged in as Staff")
with col_b:
    # --- FIXED: Added primary color layout and container width stretching ---
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.staff_authenticated = False
        st.rerun()

# (The rest of your styled donut helpers, bar graphs, and backend data calls remain EXACTLY the same down below!)