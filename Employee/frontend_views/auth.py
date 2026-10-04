import streamlit as st
from frontend_services.api_client import APIClient

def render_auth_page(api: APIClient):
    """
    Renders Authentication & User Profile Management Page.
    Streamlit Learning Focus:
    - Custom container styling and form layouts
    - st.session_state session token manipulation
    """
    st.title("🔐 Account & Access Management")

    if st.session_state.get("authenticated"):
        user = st.session_state.get("user", {})
        st.success(f"Logged in as **{user.get('user_name')}** (`{user.get('email')}`)")
        st.info(f"Assigned Access Role: **{user.get('Role', 'Employee').upper()}**")

        st.divider()
        st.subheader("🔑 Change Password")
        with st.form("change_pass_form"):
            curr_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")
            
            submit_chg = st.form_submit_button("Update Password")
            if submit_chg:
                if new_pass != confirm_pass:
                    st.error("New password and confirm password do not match.")
                elif not new_pass or not curr_pass:
                    st.error("Please fill in all password fields.")
                else:
                    status, res = api.change_password(user.get("email"), curr_pass, new_pass)
                    if status == 200 and res.get("Status") == "Success":
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error(f"Password update failed: {res.get('Message')}")

        st.divider()
        if st.button("🚪 Logout from Application", type="primary"):
            api.logout()
            st.toast("Logged out", icon="👋")
            st.rerun()

    else:
        auth_tab_login, auth_tab_reg = st.tabs(["🔒 Sign In", "📝 Register New Account"])

        with auth_tab_login:
            st.subheader("Sign In to Employee System")
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="user@example.com")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign In", use_container_width=True)

                if submit_login:
                    if not email or not password:
                        st.error("Please provide both email and password.")
                    else:
                        with st.spinner("Authenticating..."):
                            status, res = api.login(email, password)
                        if status == 200 and res.get("Status") == "Success":
                            st.toast(f"Welcome back, {res.get('Data', {}).get('user_name')}!", icon="🎉")
                            st.rerun()
                        else:
                            st.error(f"Authentication failed: {res.get('Message')}")

        with auth_tab_reg:
            st.subheader("Create New User Account")
            with st.form("register_form"):
                u_name = st.text_input("Username", placeholder="e.g. john_doe")
                u_email = st.text_input("Email", placeholder="john@example.com")
                u_pass = st.text_input("Password", type="password")
                u_role = st.selectbox("Requested Role", options=["employee", "admin", "superadmin"])

                submit_reg = st.form_submit_button("Register Account", use_container_width=True)
                if submit_reg:
                    if not u_name or not u_email or not u_pass:
                        st.error("Please fill in all required fields.")
                    else:
                        status, res = api.register(u_name, u_email, u_pass, u_role)
                        if status == 200 and res.get("Status") == "Success":
                            st.success("✅ Account created successfully! Please sign in.")
                        else:
                            st.error(f"Registration failed: {res.get('Message')}")
