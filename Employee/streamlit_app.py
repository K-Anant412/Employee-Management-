import streamlit as st
from frontend_services.api_client import APIClient
from frontend_views.dashboard import render_dashboard_page
from frontend_views.employees import render_employees_page
from frontend_views.departments import render_departments_page
from frontend_views.attendance import render_attendance_page
from frontend_views.payroll import render_payroll_page
from frontend_views.auth import render_auth_page

# Streamlit Technique 1: Page Configuration MUST be the first Streamlit command executed
st.set_page_config(
    page_title="EMS - Employee Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit Technique 2: Custom CSS injection for modern HR dashboard aesthetic
st.markdown("""
    <style>
    /* Global Container styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header card styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1e293b;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }

    /* Primary buttons styling */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }
    
    /* Form container border polish */
    div[data-testid="stForm"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit Technique 3: Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# Initialize API Client singleton
api_client = APIClient()

# Streamlit Technique 4: Sidebar Navigation and Branding
with st.sidebar:
    st.image("https://img.icons8.com/color/96/business-building.png", width=64)
    st.title("EMS Hub")
    st.caption("Enterprise Employee Operations")
    st.divider()

    # User status widget in sidebar
    if st.session_state.authenticated and st.session_state.user:
        u_name = st.session_state.user.get("user_name", "User")
        u_role = st.session_state.user.get("Role", "employee").upper()
        st.markdown(f"👤 **{u_name}**")
        st.markdown(f"🏷️ Role: `{u_role}`")
        if st.button("Logout", key="sidebar_logout", use_container_width=True):
            api_client.logout()
            st.rerun()
    else:
        st.info("🔒 Guest Mode. Log in for administrative controls.")
        if st.button("Go to Sign In", key="sidebar_login_nav", use_container_width=True):
            st.session_state.current_page = "🔐 Auth & Account"

    st.divider()
    
    # Navigation menu selection
    navigation_options = [
        "📊 Dashboard",
        "👥 Employees",
        "🏢 Departments",
        "📅 Attendance",
        "💰 Payroll",
        "🔐 Auth & Account"
    ]
    
    selected_page = st.radio(
        "Navigation Menu",
        options=navigation_options,
        index=0
    )
    
    st.divider()
    st.caption("🚀 Target Architecture:\nStreamlit Cloud → Render → Aiven MySQL")

# Router Logic: Render selected view component based on sidebar choice
if selected_page == "📊 Dashboard":
    render_dashboard_page(api_client)
elif selected_page == "👥 Employees":
    render_employees_page(api_client)
elif selected_page == "🏢 Departments":
    render_departments_page(api_client)
elif selected_page == "📅 Attendance":
    render_attendance_page(api_client)
elif selected_page == "💰 Payroll":
    render_payroll_page(api_client)
elif selected_page == "🔐 Auth & Account":
    render_auth_page(api_client)
