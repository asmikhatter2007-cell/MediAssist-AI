import streamlit as st

def render_sidebar(current_page_index):
    # Cross-theme resilient CSS supporting both high-contrast light and dark views
# Systemic Premium Style Overrides
    st.markdown(
        """
        <style>
        /* ================= 1. SIDEBAR FIXED LOCK ================= */
        /* This forces the sidebar panel to maintain a consistent dark-theme look across ALL pages */
        section[data-testid="stSidebar"], 
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 350px !important;
            max-width: 350px !important;
            background: #0D1226 !important; /* Forces it to stay uniform */
            border-right: 1px solid rgba(255,255,255,0.07) !important;
        }
        
        div[data-testid="stSidebarUserContent"] {
            padding-top: 2.5rem !important;
        }
        
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Custom Navigation Menu Tabs Layout */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            gap: 12px;
        }
        
        div[data-testid="stRadio"] [data-testid="stRadioDot"],
        div[data-testid="stRadio"] label div[dir="ltr"] {
            display: none !important;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            padding: 14px 18px !important;
            border-radius: 12px !important;
            cursor: pointer;
            transition: all 0.25s ease-in-out;
            width: 100%;
            display: flex;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            transform: translateX(4px);
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label p {
            font-size: 15px !important;
            font-weight: 500 !important;
            margin: 0 !important;
            color: #f8f9fa !important; /* Crisp white menu options */
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] {
            background-color: #0E4C92 !important;
            border-color: #0c4380 !important;
            box-shadow: 0 4px 12px rgba(14, 76, 146, 0.3);
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] p {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        /* ================= 2. METRIC TEXT VISIBILITY FIX ================= */
        /* This forces the labels of st.metric to be bright white, and the numbers to pop */
        div[data-testid="stMetricLabel"] p {
            color: #EDEFFC !important;
            font-weight: 700 !important;
            font-size: 15px !important;
        }
        
        div[data-testid="stMetricValue"] div {
            color: #2DD4BF !important; /* Bright premium teal for the numeric data */
            font-weight: 800 !important;
            font-size: 2rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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

        # Main Navigation Radio Selector
        page = st.radio(
            "Navigation Menu",
            [
                "🏠 Home", 
                "🩺 Patient Assistant Before Triage", 
                "🚑 Patient Assistant After Triage", 
                "📊 Dashboard",
                "📋 About"
            ],
            index=current_page_index,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("Select a module above to seamlessly navigate between features.")

    # Core Dynamic Router
    if page == "🏠 Home" and current_page_index != 0:
        st.switch_page("streamlit_app.py")
    elif page == "🩺 Patient Assistant Before Triage" and current_page_index != 1:
        st.switch_page("pages/1_Patient_Assistant_Before_Triage.py")
    elif page == "🚑 Patient Assistant After Triage" and current_page_index != 2:
        try:
            st.switch_page("pages/2_Patient_Assistant_After_Triage.py")
        except Exception:
            st.switch_page("pages/After_Triage.py")
    elif page == "📊 Dashboard" and current_page_index != 3:
        st.switch_page("pages/3_Dashboard.py")
    elif page == "📋 About" and current_page_index != 4:
        st.switch_page("pages/4_About.py")