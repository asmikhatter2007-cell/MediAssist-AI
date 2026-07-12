import streamlit as st

def render_sidebar(current_page_index):
    # Cross-theme resilient CSS supporting both high-contrast light and dark views
    # Systemic Premium Style Overrides
    st.markdown("""
<style>

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"]{
    width:330px !important;
    background:#0D1226 !important;
    border-right:1px solid rgba(255,255,255,.08);
}

div[data-testid="stSidebarUserContent"]{
    padding-top:2rem !important;
}

[data-testid="stSidebarNav"]{
    display:none;
}

/* Hide radio dots */

div[data-testid="stRadio"] [data-testid="stRadioDot"]{
    display:none !important;
}

div[data-testid="stRadio"] label div[dir="ltr"] > div:first-child{
    display:none !important;
}

/* Navigation cards */

div[data-testid="stRadio"] > div[role="radiogroup"]{
    gap:12px;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label{

    width:100%;
    padding:14px 18px !important;

    border-radius:14px !important;

    background:rgba(255,255,255,.05) !important;

    border:1px solid rgba(255,255,255,.08) !important;

    transition:.25s;

}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover{

    background:rgba(255,255,255,.08) !important;

    transform:translateX(5px);

}

div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"]{

    background:linear-gradient(135deg,#2563EB,#1D4ED8) !important;

    border-color:#2563EB !important;

}

div[data-testid="stRadio"] p{

    color:white !important;

    font-size:15px !important;

    font-weight:600 !important;

}

/* Sidebar collapse arrow */

[data-testid="stSidebarCollapseButton"]{

    color:white !important;

}

[data-testid="stSidebarCollapseButton"] svg{

    fill:white !important;

    stroke:white !important;

}

/* Metric visibility */

div[data-testid="stMetricLabel"] p{

    color:white !important;

}

div[data-testid="stMetricValue"]{

    color:#2DD4BF !important;

}

/* Prevent weird shifting */

[data-testid="stAppViewContainer"]{

    overflow-x:hidden;

}

main{

    transition:margin-left .25s ease;

}

</style>
""", unsafe_allow_html=True)

    with st.sidebar:
        # Centered logo and custom header text layout
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 8px;">
                <img src="https://cdn-icons-png.flaticon.com/512/822/822118.png" width="85">
                <h1 style="font-size: 30px; font-weight: 700; margin-top: 12px; margin-bottom: 0px; background: linear-gradient(45deg, #ff4b4b, #0e4c92); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MediAssist AI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")

        # Main Navigation Radio Selector - Tracks 7 pages total (0 to 6)
        page = st.radio(
            "Navigation Menu",
            [
                "🏠 Home", 
                "🧬 Patient Disease Predictor",
                "🩺 Patient Assistant Before Triage", 
                "🚑 Patient Assistant After Triage", 
                "⚙️ Admin Panel",
                "📊 Dashboard",
                "📋 About"
            ],
            index=current_page_index,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("Select a module above to seamlessly navigate between features.")

    # ================= FIXED CORE DYNAMIC ROUTER =================
    # Each condition matches the index configuration exactly
    if page == "🏠 Home" and current_page_index != 0:
        st.switch_page("streamlit_app.py")
        
    elif page == "🧬 Patient Disease Predictor" and current_page_index != 1:
        st.switch_page("pages/1_Patient_Disease_Predictor.py")
        
    elif page == "🩺 Patient Assistant Before Triage" and current_page_index != 2:
        st.switch_page("pages/2_Patient_Assistant_Before_Triage.py")
        
    elif page == "🚑 Patient Assistant After Triage" and current_page_index != 3:
        st.switch_page("pages/3_Patient_Assistant_After_Triage.py")
        
    elif page == "⚙️ Admin Panel" and current_page_index != 4:
        st.switch_page("pages/4_Admin_Panel.py")
        
    elif page == "📊 Dashboard" and current_page_index != 5:
        st.switch_page("pages/5_Dashboard.py")
        
    elif page == "📋 About" and current_page_index != 6:
        st.switch_page("pages/6_About.py")