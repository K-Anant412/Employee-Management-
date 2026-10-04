import streamlit as st
import pandas as pd
from frontend_services.api_client import APIClient

def render_employees_page(api: APIClient):
    """
    Renders the Employee Management section.
    Streamlit Learning Focus:
    - st.tabs(): Clean multi-view tab organization within a single page
    - st.form(): Prevents Streamlit from rerunning on every single input change
    - st.file_uploader(): Easy drag-and-drop CSV file intake
    - st.download_button(): Direct binary download delivery for generated PDFs
    - st.toast(): Unobtrusive success/error notifications
    """
    st.title("👥 Employee Directory & Operations")
    st.markdown("Manage employee records, search, filter, perform bulk updates, and export reports.")

    # Fetch departments list for dropdown selections
    dept_status, dept_data = api.get_departments()
    dept_options = [d["Department"] for d in dept_data.get("Data", [])] if dept_status == 200 and dept_data.get("Data") else []

    # Check user permissions from session state
    user = st.session_state.get("user", {})
    user_role = user.get("Role", "employee").lower()
    is_superadmin = (user_role == "superadmin")

    # Streamlit Technique: st.tabs() for clear workflow navigation
    tab_list, tab_add, tab_edit, tab_tools = st.tabs([
        "📋 Directory & Search",
        "➕ Add Employee",
        "✏️ Edit & Delete",
        "⚙️ CSV & Export Tools"
    ])

    # --- TAB 1: Directory & Search ---
    with tab_list:
        st.subheader("Employee Directory")
        
        # Search & Salary Filter Bar
        s_col1, s_col2, s_col3 = st.columns([2, 1, 1])
        with s_col1:
            search_query = st.text_input("🔍 Search by Name", placeholder="Type employee name...")
        with s_col2:
            min_salary = st.number_input("Min Salary (₹)", min_value=0, value=0, step=5000)
        with s_col3:
            max_salary = st.number_input("Max Salary (₹)", min_value=0, value=500000, step=10000)

        # Trigger API query based on filters
        if search_query:
            status, data = api.search_employees_by_name(search_query)
        elif min_salary > 0 or max_salary < 500000:
            status, data = api.filter_employees_by_salary(min_salary, max_salary)
        else:
            status, data = api.get_employees_ui_all()

        if status == 200 and data.get("Data"):
            records = data.get("Data")
            df = pd.DataFrame(records)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"Showing {len(records)} employee record(s).")
        else:
            msg = data.get("Message", "No matching employees found.")
            st.info(f"ℹ️ {msg}")

    # --- TAB 2: Add Employee ---
    with tab_add:
        st.subheader("Add New Employee")
        # Streamlit Technique: st.form() delays rerun until submission
        with st.form("add_employee_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
                email = st.text_input("Email Address *", placeholder="rahul@example.com")
                city = st.text_input("City *", placeholder="e.g. Mumbai")
            with f_col2:
                salary = st.number_input("Monthly Salary (₹) *", min_value=10000, value=45000, step=2000)
                department = st.selectbox("Department *", options=dept_options if dept_options else ["General"])

            submitted = st.form_submit_button("➕ Create Employee Record", use_container_width=True)
            if submitted:
                if not name or not email or not city or not department:
                    st.error("Please complete all required fields.")
                else:
                    status, res = api.create_employee(name, city, email, salary, department)
                    if status == 200 and res.get("Status") == "Success":
                        st.toast(f"✅ Employee {name} created successfully!", icon="🎉")
                        st.success(f"Employee '{name}' added successfully.")
                    else:
                        st.error(f"Failed to create employee: {res.get('Message')}")

    # --- TAB 3: Edit & Delete ---
    with tab_edit:
        st.subheader("Update or Remove Employee")
        if not is_superadmin:
            st.warning("🔒 Administrative Permission Required: Updating or deleting employees requires 'superadmin' role privileges.")
        
        # Load employees for selection
        emp_status, emp_resp = api.get_employees_ui_all()
        emp_list = emp_resp.get("Data", []) if emp_status == 200 else []

        if emp_list:
            emp_map = {f"{e['id']} - {e['name']} ({e['department']})": e for e in emp_list}
            selected_emp_key = st.selectbox("Select Employee to Manage", options=list(emp_map.keys()))
            selected_emp = emp_map[selected_emp_key]

            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.markdown("### Update Employee Details")
                with st.form("update_emp_form"):
                    up_name = st.text_input("Name", value=selected_emp.get("name", ""))
                    up_email = st.text_input("Email", value=selected_emp.get("email", ""))
                    up_salary = st.number_input("Salary (₹)", value=float(selected_emp.get("salary", 0)))
                    
                    curr_dept = selected_emp.get("department")
                    default_idx = dept_options.index(curr_dept) if curr_dept in dept_options else 0
                    up_dept = st.selectbox("Department", options=dept_options, index=default_idx)

                    update_btn = st.form_submit_button("Update Record", disabled=not is_superadmin)
                    if update_btn:
                        update_payload = {
                            "name": up_name,
                            "email": up_email,
                            "salary": up_salary,
                            "department": up_dept
                        }
                        st_code, res = api.update_employee(selected_emp["id"], update_payload)
                        if st_code == 200 and res.get("Status") == "Success":
                            st.toast("✅ Record updated!", icon="✏️")
                            st.experimental_rerun() if hasattr(st, 'experimental_rerun') else st.rerun()
                        else:
                            st.error(f"Update failed: {res.get('Message')}")

            with e_col2:
                st.markdown("### Danger Zone")
                with st.container(border=True):
                    st.write(f"**Delete employee {selected_emp['name']}?**")
                    st.caption("This action is permanent and deletes associated attendance records.")
                    if st.button("🗑️ Delete Employee", type="primary", disabled=not is_superadmin, use_container_width=True):
                        st_code, res = api.delete_employee(selected_emp["id"])
                        if st_code == 200:
                            st.toast("Employee record removed", icon="🗑️")
                            st.rerun()
                        else:
                            st.error(f"Deletion error: {res.get('Message')}")
        else:
            st.info("No employee records available.")

    # --- TAB 4: CSV & Export Tools ---
    with tab_tools:
        st.subheader("Data Tools & Reports")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### 📥 Bulk CSV Upload")
            st.caption("Upload a CSV containing: `name`, `email`, `city`, `department_id`, `salary`")
            uploaded_file = st.file_uploader("Choose CSV File", type=["csv"])
            if uploaded_file is not None:
                if st.button("Process Bulk Upload"):
                    bytes_data = uploaded_file.getvalue()
                    status, res = api.upload_employees_csv(bytes_data, uploaded_file.name)
                    if status == 200 and res.get("Status") == "Success":
                        st.success("✅ Bulk CSV upload processed successfully!")
                    else:
                        st.error(f"CSV upload failed: {res.get('Message')}")

        with c2:
            st.markdown("### 📄 Export PDF Report")
            st.caption("Generate and download a formatted PDF summary of all current employees.")
            if st.button("Generate Employee PDF"):
                with st.spinner("Generating PDF document..."):
                    pdf_bytes, err = api.download_employee_pdf()
                    if pdf_bytes:
                        st.download_button(
                            label="⬇️ Download Employees PDF",
                            data=pdf_bytes,
                            file_name="employees_report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.toast("PDF generated!", icon="📄")
                    else:
                        st.error(f"Failed to generate PDF: {err}")
