import streamlit as st
import pandas as pd
from frontend_services.api_client import APIClient

def render_payroll_page(api: APIClient):
    """
    Renders Payroll & Bonus Management Page.
    Streamlit Learning Focus:
    - st.columns() for breakdown metrics
    - Formatting currency & numerical data cleanly
    - Interactive report generation
    """
    st.title("💰 Payroll & Compensation")
    st.markdown("Generate monthly payroll, calculate attendance-based bonuses, and inspect yearly reports.")

    # Fetch employees list for dropdown selection
    emp_status, emp_data = api.get_employees_ui_all()
    employees = emp_data.get("Data", []) if emp_status == 200 else []

    p_tab_gen, p_tab_view, p_tab_yearly = st.tabs([
        "⚙️ Generate Payroll",
        "💵 View Monthly Slip",
        "📈 Yearly Bonus Report"
    ])

    # --- TAB 1: Generate Payroll ---
    with p_tab_gen:
        st.subheader("Generate Monthly Payroll")
        st.caption("Calculates net salary after attendance deductions (absent/half-days) and attendance bonus rewards.")

        if employees:
            emp_dict = {f"{e['id']} - {e['name']} (₹{e['salary']:,}/mo)": e['id'] for e in employees}
            selected_label = st.selectbox("Select Employee to Process", options=list(emp_dict.keys()), key="gen_payroll_select")
            emp_id = emp_dict[selected_label]

            if st.button("🚀 Calculate & Finalize Payroll", type="primary", use_container_width=True):
                with st.spinner("Processing attendance records and computing compensation..."):
                    gen_status, gen_res = api.generate_payroll(emp_id)

                if gen_status == 200 and gen_res.get("Status") == "Success":
                    p_data = gen_res.get("Data", {})
                    st.toast("Payroll generated successfully!", icon="💵")
                    st.success(f"Payroll finalized for **{p_data.get('Employee Name')}**")

                    # Display calculated slip metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Base Monthly Salary", f"₹ {p_data.get('Monthly Salary', 0):,.2f}")
                    m2.metric("Total Deductions", f"₹ {p_data.get('Total Deduction', 0):,.2f}")
                    m3.metric("Attendance Bonus", f"₹ {p_data.get('Bonus', 0):,.2f}")
                    m4.metric("Final Net Salary", f"₹ {p_data.get('Final Salary', 0):,.2f}", delta="Net Payout")

                    st.divider()
                    with st.expander("🔍 Inspection & Attendance Calculation Details", expanded=True):
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            st.write(f"**Present Days:** `{p_data.get('Present Days')}`")
                            st.write(f"**Absent Days:** `{p_data.get('Absent Days')}`")
                            st.write(f"**Half Days:** `{p_data.get('Half Days')}`")
                            st.write(f"**Paid Leaves Allowed:** `{p_data.get('Paid Leaves')}`")
                        with d_col2:
                            st.write(f"**Unpaid Leaves Charged:** `{p_data.get('Unpaid Leaves')}`")
                            st.write(f"**Attendance Score:** `{p_data.get('Attendance Percentage')}%`")
                            st.write(f"**Bonus Tier:** `{'20%' if p_data.get('Attendance Percentage', 0)>=95 else ('15%' if p_data.get('Attendance Percentage', 0)>=90 else ('10%' if p_data.get('Attendance Percentage', 0)>=80 else '0%'))}`")
                else:
                    st.error(f"Payroll processing error: {gen_res.get('Message')}")
        else:
            st.info("No employee records found.")

    # --- TAB 2: View Monthly Slip ---
    with p_tab_view:
        st.subheader("Monthly Salary Slip Lookup")
        if employees:
            emp_dict_view = {f"{e['id']} - {e['name']}": e['id'] for e in employees}
            v_label = st.selectbox("Select Employee", options=list(emp_dict_view.keys()), key="view_payroll_select")
            v_id = emp_dict_view[v_label]

            if st.button("Fetch Current Month Slip"):
                v_status, v_res = api.get_employee_payroll(v_id)
                if v_status == 200 and v_res.get("Status") == "Success":
                    slip = v_res.get("Data", {})
                    st.write(f"### Salary Slip - {slip.get('Employee Name')} (Month {slip.get('Month')}/{slip.get('Year')})")
                    
                    s_c1, s_c2, s_c3 = st.columns(3)
                    s_c1.metric("Base Salary", f"₹ {slip.get('Total Salary', 0):,.2f}")
                    s_c2.metric("Deductions", f"₹ {slip.get('Total Deduction', 0):,.2f}")
                    s_c3.metric("Net Salary Paid", f"₹ {slip.get('Final Salary', 0):,.2f}")
                else:
                    st.info(f"ℹ️ {v_res.get('Message', 'No payroll generated for this month yet.')}")
        else:
            st.info("No employee records available.")

    # --- TAB 3: Yearly Bonus Report ---
    with p_tab_yearly:
        st.subheader("Yearly Compensation & Bonus Report")
        if employees:
            emp_dict_yr = {f"{e['id']} - {e['name']}": e['id'] for e in employees}
            y_label = st.selectbox("Select Employee", options=list(emp_dict_yr.keys()), key="yearly_bonus_select")
            y_id = emp_dict_yr[y_label]

            if st.button("Generate Yearly Report"):
                y_status, y_res = api.get_yearly_bonus(y_id)
                if y_status == 200 and y_res.get("Status") == "Success":
                    y_data = y_res.get("Data", {})
                    st.markdown(f"### Annual Earnings Report: **{y_data.get('Employee Name')}** ({y_data.get('Year')})")
                    
                    yb1, yb2 = st.columns(2)
                    yb1.metric("Total Annual Salary Paid", f"₹ {y_data.get('Total Yearly Salary', 0):,.2f}")
                    yb2.metric("Total Annual Bonus Received", f"₹ {y_data.get('Total Yearly Bonus', 0):,.2f}")

                    st.divider()
                    reports = y_data.get("Monthly Reports", [])
                    if reports:
                        df_m = pd.DataFrame(reports)
                        df_m.columns = ["Month", "Net Salary (₹)", "Bonus Earned (₹)"]
                        st.dataframe(df_m, use_container_width=True, hide_index=True)
                    else:
                        st.info("No monthly payroll entries recorded for this year yet.")
                else:
                    st.error(f"Report error: {y_res.get('Message')}")
        else:
            st.info("No employees available.")
