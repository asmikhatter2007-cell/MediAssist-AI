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

# FIXED: navigation.py only has 5 pages (indices 0-4).
# Order was 0=Home, 1=Before Triage, 2=After Triage, 3=Dashboard, 4=About
render_sidebar(3)

BASE_URL = "https://mediassist-ai-68lg.onrender.com"

# TODO: move this to an environment variable before final submission -
# a hardcoded password in a public GitHub repo is visible to anyone.
# e.g. STAFF_PASSWORD = os.environ.get("STAFF_PASSWORD", "staff123")
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

.stButton>button{
    width:100% !important; border-radius:16px !important; height:58px !important;
    background: linear-gradient(90deg, #2DD4BF 0%, #818CF8 50%, #F472B6 100%) !important;
    background-size: 200% auto !important; color:#0C1024 !important; font-size:19px !important; font-weight:800 !important; border:none !important;
    box-shadow: 0 14px 34px rgba(129,140,248,0.30) !important; transition: all 0.25s ease !important;
}
.stButton>button p{ color:#0C1024 !important; font-weight:800 !important; }
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

        # Center the login button inside the card
        _, btn_col, _ = st.columns([1.5, 1, 1.5])
        with btn_col:
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
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.staff_authenticated = False
        st.rerun()


# ---------------- CARD HELPERS ----------------

def metric_card(icon, label, value, color):
    # Kept as a single-line string on purpose — multi-line indented f-strings
    # get misread as Markdown code blocks and render as raw tags.
    return f'<div class="metric-card"><div class="metric-icon" style="background:{color}26;color:{color};">{icon}</div><div><div class="metric-header">{label}</div><div class="metric-value">{value}</div></div></div>'


def styled_bar(df, x_col, y_col, color_map, title):
    fig = px.bar(
        df, x=y_col, y=x_col, orientation="h",
        color=x_col, color_discrete_map=color_map, text=y_col
    )
    max_val = df[y_col].max()
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=15, color="#EEF1FB", family="Inter"),
        marker_line_width=0, width=0.5
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#EDEFFC")),
        height=280, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#C3CAE8", family="Inter"),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, title=None,
                   range=[0, max_val * 1.35]),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(size=13, color="#EEF1FB"),
                   automargin=True),
        margin=dict(l=10, r=20, t=45, b=10)
    )
    return fig


def styled_donut(df, label_col, value_col, color_map, title, key):
    fig = px.pie(
        df, names=label_col, values=value_col, hole=0.66,
        color=label_col, color_discrete_map=color_map
    )
    fig.update_traces(
        textinfo="none",
        marker=dict(line=dict(color="#0C1024", width=4))
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#EDEFFC")),
        height=220, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=45, b=10)
    )

    _, mid, _ = st.columns([1, 6, 1])
    with mid:
        st.plotly_chart(fig, use_container_width=True, theme=None, key=key)

    rows = []
    for label, value in zip(df[label_col], df[value_col]):
        color = color_map[label]
        row = f'<div style="display:flex;align-items:center;gap:8px;margin:4px 0;"><div style="width:10px;height:10px;border-radius:3px;background:{color};"></div><div style="font-size:13.5px;color:#EEF1FB;">{label}</div><div style="margin-left:auto;font-size:14px;font-weight:700;color:{color};">{value}</div></div>'
        rows.append(row)

    legend_html = f'<div style="padding:0 12px;">{"".join(rows)}</div>'
    st.markdown(legend_html, unsafe_allow_html=True)


# ---------------- FETCH REAL DATA FROM BACKEND ----------------
try:
    response = requests.get(f"{BASE_URL}/admin/hospital_data")
    response.raise_for_status()
    data = response.json()
except Exception:
    data = None
    st.error("Backend is not running.")

if data is not None and not data.get("has_data"):
    st.warning("No hospital data has been submitted by admin yet.")

elif data is not None:
    admin_data = data["admin_data"]
    status = data["predicted_status"]
    status_message = data["predicted_status_message"]

    status_class = {
        "Functional": "status-functional",
        "Overcrowded": "status-busy",
        "Overwhelmed": "status-overwhelmed",
    }.get(status, "status-busy")

    status_icon = {"Functional": "🟢", "Overcrowded": "🟠", "Overwhelmed": "🔴"}.get(status, "🟠")

    st.markdown(
        f'<div class="status-pill {status_class}">{status_icon} System Status: {status}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Last Updated: {admin_data['last_updated']}")
    st.caption(status_message)

    # ---------------- METRIC CARDS (row 1) ----------------
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True, key="card_patients"):
            st.markdown(metric_card("🧑‍🤝‍🧑", "Patients in ED", admin_data["current_patients_ed"], "#2DD4BF"), unsafe_allow_html=True)
    with c2:
        with st.container(border=True, key="card_beds"):
            st.markdown(metric_card("🛏️", "Beds Available", admin_data["beds_available"], "#818CF8"), unsafe_allow_html=True)
    with c3:
        with st.container(border=True, key="card_boarding"):
            st.markdown(metric_card("🚪", "Boarding in ED", admin_data["patients_boarding_ed"], "#FBBF6E"), unsafe_allow_html=True)
    with c4:
        with st.container(border=True, key="card_avgboard"):
            st.markdown(metric_card("⏱️", "Boarding Hrs", admin_data["avg_boarding_hours"], "#F472B6"), unsafe_allow_html=True)

    st.write("")

    # ---------------- METRIC CARDS (row 2) ----------------
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        with st.container(border=True, key="card_doctor"):
            st.markdown(metric_card("🩺", "Total Doctors", admin_data["total_doctors"], "#2DD4BF"), unsafe_allow_html=True)
    with c6:
        with st.container(border=True, key="card_nurse"):
            st.markdown(metric_card("👩‍⚕️", "Total Nurses", admin_data["total_nurses"], "#818CF8"), unsafe_allow_html=True)
    with c7:
        with st.container(border=True, key="card_lab"):
            st.markdown(metric_card("🧪", "Pending Labs", admin_data["pending_lab_orders"], "#FBBF6E"), unsafe_allow_html=True)
    with c8:
        with st.container(border=True, key="card_image"):
            st.markdown(metric_card("🩻", "Pending Imaging", admin_data["pending_imaging_orders"], "#F472B6"), unsafe_allow_html=True)

    st.write("")

    # ---------------- VISUAL INSIGHTS ----------------
    st.subheader("📈 Visual Insights")

    vcol1, vcol2, vcol3 = st.columns(3)

    with vcol1:
        with st.container(border=True):
            load_df = pd.DataFrame({
                "Metric": ["Patients in ED", "Beds Available", "Boarding in ED"],
                "Count": [
                    admin_data["current_patients_ed"],
                    admin_data["beds_available"],
                    admin_data["patients_boarding_ed"]
                ]
            })
            fig = styled_bar(load_df, "Metric", "Count", {
                "Patients in ED": "#2DD4BF",
                "Beds Available": "#818CF8",
                "Boarding in ED": "#F472B6"
            }, "ED Load")
            st.plotly_chart(fig, use_container_width=True, theme=None)

    with vcol2:
        with st.container(border=True):
            staff_df = pd.DataFrame({
                "Role": ["Doctors", "Nurses"],
                "Count": [admin_data["total_doctors"], admin_data["total_nurses"]]
            })
            styled_donut(staff_df, "Role", "Count", {
                "Doctors": "#2DD4BF", "Nurses": "#A78BFA"
            }, "Staffing Split", key="staff_donut")

    with vcol3:
        with st.container(border=True):
            orders_df = pd.DataFrame({
                "Type": ["Lab Orders", "Imaging Orders"],
                "Pending": [admin_data["pending_lab_orders"], admin_data["pending_imaging_orders"]]
            })
            styled_donut(orders_df, "Type", "Pending", {
                "Lab Orders": "#FBBF24", "Imaging Orders": "#FB7185"
            }, "Pending Orders Split", key="orders_donut")