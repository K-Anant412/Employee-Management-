import streamlit as st
import pandas as pd
from frontend_services.api_client import APIClient

def render_dashboard_page(api: APIClient):
    """
    Renders the Executive HR Dashboard page.
    Streamlit Learning Focus:
    - st.columns(): Layout metrics side-by-side in responsive grids
    - st.metric(): Standardized key performance indicator cards
    - st.bar_chart() / pandas: Native chart rendering
    - st.container() & st.expander(): Structured section styling
    """
    st.title("📊 HR Executive Dashboard")
    st.markdown("Overview of key organization metrics, workforce distribution, and quick operations.")
    st.divider()

    # Fetch data from Flask REST API
    with st.spinner("Fetching live organizational metrics..."):
        emp_status, emp_data = api.get_employees_ui_all()
        dept_status, dept_data = api.get_departments_with_employee_counts()

    employees_list = emp_data.get("Data", []) if emp_status == 200 else []
    departments_list = dept_data.get("Data", []) if dept_status == 200 else []

    # Calculate summary metrics
    total_employees = len(employees_list)
    total_departments = len(departments_list)

    df_emp = pd.DataFrame(employees_list) if employees_list else pd.DataFrame()
    total_payroll = df_emp["salary"].sum() if not df_emp.empty and "salary" in df_emp.columns else 0
    avg_salary = df_emp["salary"].mean() if not df_emp.empty and "salary" in df_emp.columns else 0

    # Streamlit Technique: st.columns() for horizontal KPI summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Workforce", value=f"{total_employees} Active", delta="Staff Count")

    with col2:
        st.metric(label="Departments", value=f"{total_departments}", delta="Active Teams")

    with col3:
        st.metric(label="Monthly Payroll", value=f"₹ {total_payroll:,.2f}", delta="Estimated")

    with col4:
        st.metric(label="Average Salary", value=f"₹ {avg_salary:,.2f}", delta="Per Employee")

    st.divider()

    # Visualizations section
    chart_col, info_col = st.columns([2, 1])

    with chart_col:
        st.subheader("🏢 Department Headcount Distribution")
        if departments_list:
            df_dept = pd.DataFrame(departments_list)
            # Standardize column names for chart rendering
            df_chart = df_dept.set_index("Department")[["Employees"]]
            st.bar_chart(df_chart, color="#2563eb")
        else:
            st.info("No department data available yet.")

    with info_col:
        st.subheader("⚡ Quick Insights")
        with st.container(border=True):
            st.markdown(f"**Highest Department Headcount:**")
            if departments_list:
                top_dept = max(departments_list, key=lambda x: x.get("Employees", 0))
                st.write(f"🏆 **{top_dept.get('Department')}** ({top_dept.get('Employees')} members)")
            else:
                st.write("N/A")

            st.markdown("---")
            st.markdown("**Top Earning Tier:**")
            if not df_emp.empty and "salary" in df_emp.columns:
                max_emp = df_emp.loc[df_emp['salary'].idxmax()]
                st.write(f"⭐ **{max_emp.get('name')}** (₹ {max_emp.get('salary'):,.0f})")
            else:
                st.write("N/A")

    st.divider()

    # Recent Employee Directory Snapshot
    st.subheader("📋 Recent Employee Additions")
    if not df_emp.empty:
        display_df = df_emp[["id", "name", "email", "department", "salary", "city"]].tail(5)
        display_df.columns = ["ID", "Name", "Email", "Department", "Salary (₹)", "City"]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No employee records found in the system.")
