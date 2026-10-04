import streamlit as st
import pandas as pd
from frontend_services.api_client import APIClient

def render_departments_page(api: APIClient):
    """
    Renders Department Management Page.
    Streamlit Learning Focus:
    - st.expander(): Accordion collapsible sections to save vertical screen space
    - Role-based conditional UI components (disabling buttons based on permissions)
    """
    st.title("🏢 Department Management")
    st.markdown("Create departments, monitor staffing allocations, and edit organization units.")

    # Get user role for permission checks
    user = st.session_state.get("user", {})
    user_role = user.get("Role", "employee").lower()
    is_superadmin = (user_role == "superadmin")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Existing Departments & Workforce Distribution")
        status, data = api.get_departments_with_employee_counts()
        
        if status == 200 and data.get("Data"):
            dept_list = data.get("Data", [])
            df_dept = pd.DataFrame(dept_list)
            df_dept.columns = ["Department ID", "Department Name", "Assigned Employees"]
            
            st.dataframe(
                df_dept,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No departments found. Use the form to add one.")

    with col2:
        st.subheader("➕ Create New Department")
        if not is_superadmin:
            st.info("ℹ️ Adding a new department requires 'superadmin' role.")
            
        with st.form("add_department_form", clear_on_submit=True):
            dept_name = st.text_input("Department Name *", placeholder="e.g. Engineering")
            submit_dept = st.form_submit_button("Create Department", disabled=not is_superadmin, use_container_width=True)
            
            if submit_dept:
                if not dept_name.strip():
                    st.error("Department name cannot be empty.")
                else:
                    st_code, res = api.create_department(dept_name.strip())
                    if st_code == 200:
                        st.toast(f"✅ Department '{dept_name}' created!", icon="🏢")
                        st.rerun()
                    else:
                        st.error(f"Failed to create department: {res.get('Message')}")

    st.divider()

    st.subheader("⚙️ Department Operations & Maintenance")
    # Streamlit Technique: st.expander() for collapsible options
    with st.expander("✏️ Rename or Remove Department", expanded=False):
        d_status, d_data = api.get_departments()
        all_depts = d_data.get("Data", []) if d_status == 200 else []

        if all_depts:
            dept_map = {f"{d['Id']} - {d['Department']}": d for d in all_depts}
            selected_key = st.selectbox("Select Department", options=list(dept_map.keys()))
            selected_dept = dept_map[selected_key]

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                new_name = st.text_input("New Department Name", value=selected_dept["Department"])
                if st.button("Update Department Name"):
                    code, res = api.update_department(selected_dept["Id"], new_name)
                    if code == 200 and res.get("Status") == "Success":
                        st.toast("Department name updated!", icon="✏️")
                        st.rerun()
                    else:
                        st.error(f"Update failed: {res.get('Message')}")

            with m_col2:
                st.write("**Delete Department**")
                st.caption("Departments with assigned employees cannot be deleted.")
                if st.button("Delete Department", type="primary", disabled=not is_superadmin):
                    code, res = api.delete_department(selected_dept["Id"])
                    if code == 200 and res.get("Status") == "Success":
                        st.toast("Department deleted!", icon="🗑️")
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {res.get('Message')}")
        else:
            st.info("No departments available.")
