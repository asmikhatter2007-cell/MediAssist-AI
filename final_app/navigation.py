import streamlit as st

def render_sidebar(current_page_index):
    # Advanced CSS to adjust sidebar width, hide default nav, and style custom tabs
    st.markdown(
        """
        <style>
        /* Make the sidebar wider (default is 336px) */
        [data-testid="stSidebar"][aria-expanded="true"]{
            min-width: 350px !important;
            max-width: 350px !important;
        }
        
        /* Hide default Streamlit navigation links */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Style the Radio Group Container */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            gap: 10px;
        }
        
        /* Hide the ugly circular radio buttons */
        div[data-testid="stRadio"] [data-testid="stRadioDot"] {
            display: none !important;
        }
        
        /* Style each option item to look like a modern button/tab */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 12px 16px !important;
            border-radius: 10px !important;
            cursor: pointer;
            transition: all 0.25s ease-in-out;
            width: 100%;
            display: flex;
            align-items: center;
        }
        
        /* Hover animation effect */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            background-color: #e9ecef;
            transform: translateX(4px);
            border-color: #ced4da;
        }
        
        /* Active / Selected tab styling */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-baseweb="radio"] div[dir="ltr"] {
            background-color: #0E4C92 !important;
            color: white !important;
            border-radius: 10px;
        }
        
        /* Fix text color inside the active selected tab */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] p {
            color: #0E4C92 !important;
            font-weight: 600 !important;
        }
        
        /* Clean up sidebar padding */
        div[data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 5px;">
                <img src="https://cdn-icons-png.flaticon.com/512/2967/2967350.png" width="90">
                <h1 style="color: #31333F; font-size: 26px; margin-top: 10px; margin-bottom: 0px;">MediAssist AI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Updated Navigation Options
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

    # Shared Routing Logic
    if page == "🏠 Home" and current_page_index != 0:
        st.switch_page("streamlit_app.py")
    elif page == "🩺 Patient Assistant Before Triage" and current_page_index != 1:
        st.switch_page("pages/1_Patient_Assistant_Before_Triage.py")
    elif page == "🚑 Patient Assistant After Triage" and current_page_index != 2:
        st.switch_page("pages/2_Patient_Assistant_After_Triage.py")
    elif page == "📊 Dashboard" and current_page_index != 3:
        st.switch_page("pages/3_Dashboard.py")
    elif page == "📋 About" and current_page_index != 4:
        st.switch_page("pages/4_About.py")