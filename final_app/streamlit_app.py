import streamlit as st
from navigation import render_sidebar

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🏥",
    layout="wide",
)
render_sidebar(0)

# ---------------- DARK THEME & TOP SPACING FIX ----------------
st.markdown("""
<style>
header[data-testid="stHeader"]{ background: #0C1024 !important; }
[data-testid="stToolbar"]{ background: transparent !important; }
html, body{ background: #0C1024 !important; }
.block-container{ padding-top: 4.5rem !important; max-width: 1200px; }

.stApp{
    background:
        radial-gradient(circle at 10% 5%, rgba(129,140,248,0.16), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(45,212,191,0.16), transparent 42%),
        linear-gradient(160deg, #0B0F22 0%, #101833 50%, #0C1024 100%);
    color: #EEF1FB;
}

/* FIX: Splits up the title to isolate emoji graphics from being masked as a solid cyan block */
.title-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-bottom: 5px;
}
.title-icon {
    font-size: 3.5rem;
}
.hero-title {
    background: linear-gradient(90deg, #2DD4BF, #818CF8 55%, #F472B6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    margin-bottom: 0px;
    display: inline-block;
}
.hero-subtitle { color: #EDEFFC !important; font-weight: 700 !important; text-align: center; margin-top: 10px; }
.hero-desc { text-align: center; font-size: 18px; color: #9BA3C7 !important; margin-bottom: 30px; }

div[data-testid="stVerticalBlockBorderWrapper"]{
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(18px);
    border-radius: 22px !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    padding: 24px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}
div[data-testid="stVerticalBlockBorderWrapper"] p { color: #EEF1FB !important; }
li { color: #C3CAE8 !important; margin-bottom: 8px; }
h3 { color: #EDEFFC !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="title-container">
    <span class="title-icon">🏥</span>
    <h1 class="hero-title">MediAssist AI</h1>
</div>
""", unsafe_allow_html=True)
st.markdown('<h3 class="hero-subtitle">AI-Powered Emergency Department Decision Support System</h3>', unsafe_allow_html=True)
st.markdown('<p class="hero-desc">Helping patients make smarter emergency decisions before and after triage.</p>', unsafe_allow_html=True)

st.write("")

# ---------------- INTRO ----------------
with st.container(border=True):
    st.markdown("### Welcome")
    st.markdown("MediAssist AI is an intelligent healthcare support platform that assists patients during emergency visits by predicting:")
    st.markdown("- 🩺 Disease / Department Recommendation")
    st.markdown("- 🏥 Hospital Overcrowding Status")
    st.markdown("- ⏳ Estimated Waiting Time")
    st.markdown("- 🚑 Admission Probability")

st.write("")

# ---------------- STAGES CONFIGURATION ----------------
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("### 🩺 Stage 1 — Before Triage")
        st.markdown("This stage helps patients decide:")
        st.markdown("✅ **Which department to visit**")
        st.markdown("✅ **Hospital crowd level**")
        st.markdown("✅ **Estimated triage waiting time**")

with col2:
    with st.container(border=True):
        st.markdown("### 🚑 Stage 2 — After Triage")
        st.markdown("Once triage is completed:")
        st.markdown("✅ **Updated hospital status**")
        st.markdown("✅ **Doctor waiting time**")
        st.markdown("✅ **Admission likelihood**")
    
st.write("")
st.markdown("---")
st.caption("Developed as an AI-powered Emergency Department Decision Support System using Machine Learning, FastAPI and Streamlit.")