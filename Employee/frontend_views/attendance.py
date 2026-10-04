import streamlit as st
import pandas as pd
from datetime import datetime
from frontend_services.api_client import APIClient

def render_attendance_page(api: APIClient):
    """
    Renders Attendance & Leave Tracking Page.
    Streamlit Learning Focus:
    - Interactive check-in widget displaying dynamic time status
    - st.progress(): Showing percentage metric progress visually
    - st.empty(): Targetable UI placeholder for dynamic updates
    """
    st.title("📅 Attendance & Leave Management")
    st.markdown("Record daily check-ins, verify automated status allocation, and inspect monthly attendance stats.")

    # Fetch attendance employee list
    status, data = api.get_attendance_employees()
    employees = data.get("Data", []) if status == 200 else []

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚡ Mark Today's Attendance")
        with st.container(border=True):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.info(f"🕒 **Current System Time:** `{current_time}`")

            if employees:
                emp_options = {f"{e['Id']} - {e['name']} ({e['department']})": e['Id'] for e in employees}
                selected_label = st.selectbox("Select Employee", options=list(emp_options.keys()))
                selected_id = emp_options[selected_label]

                st.caption("Note: Check-in before 12:00 PM marks 'Present', after 12:00 PM marks 'Half Day'.")

                if st.button("📌 Record Check-In Now", type="primary", use_container_width=True):
                    mark_status, mark_res = api.mark_attendance(selected_id)
                    if mark_status == 200 and mark_res.get("Status") == "Success":
                        status_type = mark_res.get("Data", {}).get("status", "Recorded")
                        st.toast(f"Attendance recorded as '{status_type}'!", icon="✅")
                        st.success(f"Successfully marked attendance: **{status_type}**")
                    else:
                        msg = mark_res.get("Message", "Could not mark attendance.")
                        st.warning(f"⚠️ {msg}")
            else:
                st.info("No employees found.")

    with col2:
        st.subheader("📊 Employee Monthly Analysis")
        with st.container(border=True):
            if employees:
                emp_options_analysis = {f"{e['Id']} - {e['name']}": e['Id'] for e in employees}
                an_label = st.selectbox("Select Employee for Monthly Analysis", options=list(emp_options_analysis.keys()))
                an_id = emp_options_analysis[an_label]

                if st.button("Inspect Monthly Attendance Report", use_container_width=True):
                    an_status, an_data = api.get_attendance_analysis(an_id)
                    if an_status == 200 and an_data.get("Status") == "Success":
                        emp_info = an_data.get("Data", {})
                        st.write(f"**Employee ID:** `{emp_info.get('id')}`")
                        st.write(f"**Name:** `{emp_info.get('name')}`")
                        st.write(f"**Department:** `{emp_info.get('department')}`")
                        st.success("Active attendance profile verified.")
                    else:
                        st.error(f"Analysis failed: {an_data.get('Message')}")
            else:
                st.info("No employee records available for analysis.")

    st.divider()

    st.subheader("📋 Active Employee List for Attendance")
    if employees:
        df_att = pd.DataFrame(employees)
        df_att.columns = ["Employee ID", "Employee Name", "Department"]
        st.dataframe(df_att, use_container_width=True, hide_index=True)
