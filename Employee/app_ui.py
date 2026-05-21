import streamlit as st
import requests
import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
AUTH_URL = "http://127.0.0.1:5001/api/v1/auth"

base_url = "http://127.0.0.1:5001/api/v1"

st.set_page_config(page_title="Employee Dashboard", layout="wide")

def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


path_to_img = r"C:\Users\nohi4\OneDrive\Pictures\A\bg1.png"
if os.path.exists(path_to_img):
    bin_str = get_base64(path_to_img)
    st.markdown(
        f"""
            <style>
            .stApp {{
                    background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{bin_str}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    transform: scaleX(-1);
                    }}
            .stApp > div{{
                    transform: scaleX(-1);    
                    }}
            [data-testid="stSidebar"] {{
                background: rgba(0, 0, 0, 0.35);
                backdrop-filter: blur(12px);
            }}
            </style>
            """,
        unsafe_allow_html=True,
    )


def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None


def login_user(email, password):
    try:
        response = requests.post(
            f"{AUTH_URL}/login", json={"email": email, "password": password}
        )
        if response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.user_data = response.json().get("Data", {})
            st.rerun()
        else:
            st.error("Invalid credentials")
    except Exception as e:
        st.error(f"Connection Error: {e}")


def register_user(username, email, password, role):
    payload = {
        "user_name": username,
        "email": email,
        "password": password,
        "role": role,
    }
    try:
        response = requests.post(f"{AUTH_URL}/Register", json=payload)
        if response.status_code == 200:
            st.success("Registration Successful! Please Login.")
        else:
            st.error(response.json().get("message", "Registration Failed"))
    except Exception as e:
        st.error(f"Connection Error: {e}")


def auth_page():

        st.title(" Employee Management System")
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                if submit:
                    login_user(email, password)

        with tab2:
            with st.form("reg_form"):
                u_name = st.text_input("Full Name")
                u_email = st.text_input("Email")
                u_pass = st.text_input("Password", type="password")
                u_role = st.selectbox("Role", ["Employee", "Admin", "Superadmin"])
                submit_reg = st.form_submit_button("Create Account")
                if submit_reg:
                    register_user(u_name, u_email, u_pass, u_role)


def main_dashboard():
    with st.sidebar:
        user_name = st.session_state.user_data.get('user_name', 'User')
        st.markdown(
            f"""
            <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; margin-bottom:20px; border:1px solid #d1d5db">
                <h4 style="margin:0;">👤 {st.session_state.user_data.get('user_name', 'User')}</h4>
                <p style="color:gray; font-size:14px; margin:0;">Role: {st.session_state.user_data.get('Role', 'N/A')}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        st.subheader("Management")
        choice = st.radio("Go to:", ["Employee", "Department", "Attendance", "Salary"])
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

    if choice == "Employee":
        st.title("Employee Management")
        
        employee_url = f"{base_url}/employee"
        tab1, tab2, tab3, tab4 = st.tabs(["Home", "Manage", "Employee List", "Search"])

        with tab1:
            BASE_URL = "http://127.0.0.1:5001/api/v1"

            st.subheader("Employee Dashboard")
            st.caption("Manage employees, analytics, reports, and departments.")

            st.divider()

            response = requests.get(
                f"{BASE_URL}/employee/show_all_employees"
            )
            data = response.json()
            employees = data.get("Data", [])
            df = pd.DataFrame(employees)

            if not df.empty:
                total_emp = len(df)
                avg_salary = round(df["salary"].astype(float).mean(), 2)
                max_salary = df["salary"].astype(float).max()
                total_departments = df["department"].nunique()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Employees", total_emp)
                with col2:
                    st.metric("Departments", total_departments)
                with col3:
                    st.metric("Average Salary", f"₹ {avg_salary}")
                with col4:
                    st.metric("Highest Salary", f"₹ {max_salary}")

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Employee Distribution")
                dept_data = df["department"].value_counts()

                fig, ax = plt.subplots(figsize=(5, 4))

                colors = [
                        "#0F4C81",  
                        "#1D70A2",  
                        "#2E86C1",  
                        "#5DADE2",  
                        "#85C1E9",  
                        "#AED6F1"   
                    ]
                
                ax.pie(
                    dept_data,
                    labels=dept_data.index,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors
                )

                ax.axis("equal")  
                st.pyplot(fig, use_container_width=True)
            with col2:
                st.subheader("Salary Distribution")
                salary_data = df["salary"].astype(float).reset_index(drop=True)

                fig, ax = plt.subplots(figsize=(6, 3.5))

                ax.plot(
                    salary_data,
                    marker="o",
                    linewidth=2
                )

                ax.set_title("Employee Salaries")
                ax.set_xlabel("Employee Index")
                ax.set_ylabel("Salary")

                ax.grid(True)

                st.pyplot(fig, use_container_width=True)

        with tab2:
            st.subheader("Manage Employees")

            choice = st.selectbox(
                "select option here",
                options=[
                    "Add Employee",
                    "Update Employee",
                    "Remove Employee",
                    "Reports",
                ],
            )
            if choice == "Add Employee":
                c1, c2 = st.columns(2)

                with st.form("add_form"):
                    with c1:
                        name = st.text_input("name")
                        city = st.text_input("city")
                        salary = st.number_input("salary", min_value=0)
                    with c2:
                        email = st.text_input("email")
                        department = st.text_input("department")
                    submit = st.form_submit_button("Add Employee")

                    if submit:
                        data = {
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department,
                        }
                        try:
                            response = requests.post(
                                f"{employee_url}/add_employee", json=data
                            )
                            if response.status_code == 200:
                                st.success("New employee added")
                            else:
                                st.error("Failed to add user.")
                        except Exception as e:
                            st.error(f"Server Error: {e}")
            
            elif choice == "Update Employee":
                emp_id = st.number_input("Employee ID", min_value=1, step=1)
                fetch_url = f"{employee_url}/employee_by_id/{emp_id}"
                update_url = f"{employee_url}/update_employee/{emp_id}"

                if st.button("Fetch Employee"):
                    response = requests.get(fetch_url)
                    if response.status_code == 200:
                        raw_data = response.json()
                        if "Data" in raw_data:
                            st.session_state.employee = raw_data["Data"]
                        else:
                            st.error("Employee data not found")
                    else:
                        st.error("Employee not found")

                if "employee" in st.session_state:
                    employee = st.session_state.employee
                    c1, c2 = st.columns(2)
                    with c1:
                        name = st.text_input("Name", value=employee.get("name", ""))
                        city = st.text_input("City", value=employee.get("city", ""))
                        salary = st.number_input(
                            "Salary", min_value=0, value=int(employee.get("salary", 0))
                        )
                    with c2:
                        email = st.text_input("Email", value=employee.get("email", ""))
                        department = st.text_input(
                            "Department", value=employee.get("department", "")
                        )

                    if st.button("Save Changes"):
                        params = {
                            "name": name,
                            "city": city,
                            "email": email,
                            "salary": salary,
                            "department": department,
                        }
                        response = requests.put(update_url, json=params)
                        if response.status_code == 200:
                            st.session_state.employee = params
                        else:
                            st.error(response.text)
            
            elif choice == "Remove Employee":
                
                emp_id_delete = st.number_input(
                    "Employee ID",
                    min_value=0,
                    key="delete_employee"
                )

                if "show_delete_section" not in st.session_state:
                    st.session_state.show_delete_section = False

                if "employee_data" not in st.session_state:
                    st.session_state.employee_data = None

                url = f"{employee_url}/employee_by_id/{emp_id_delete}"
                delete_url = f"{employee_url}/delete_employee/{emp_id_delete}"


                if st.button("Remove"):
                    response = requests.get(url)

                    if response.status_code == 200:
                        raw_data = response.json()

                        if raw_data.get("Data"):
                            st.session_state.employee_data = raw_data["Data"]
                            st.session_state.show_delete_section = True
                        else:
                            st.error("Employee not found")

                if st.session_state.show_delete_section:
                    employee = st.session_state.employee_data

                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input(
                            "Name",
                            value=employee.get("name", ""),
                            disabled=True
                        )
                        st.text_input(
                            "City",
                            value=employee.get("city", ""),
                            disabled=True
                        )
                        st.number_input(
                            "Salary",
                            value=int(employee.get("salary", 0)),
                            disabled=True
                        )
                    with c2:
                        st.text_input(
                            "Email",
                            value=employee.get("email", ""),
                            disabled=True
                        )
                        st.text_input(
                            "Department",
                            value=employee.get("department", ""),
                            disabled=True
                        )
                        
                    if st.button("Delete Employee"):
                        result = requests.delete(delete_url)

                        if result.status_code == 200:
                            st.success("Employee Deleted")
                            st.session_state.show_delete_section = False
                            st.session_state.employee_data = None
                        else:
                            st.error("Delete Failed")
                            st.write(result.json())
                                    
            elif choice == "Reports":
                API_URL = f"{employee_url}/get_pdf_data"

                if st.button("Download Employee PDF"):
                    response = requests.get(API_URL)
                    
                    if response.status_code == 200:
                        st.download_button(
                            label="Click Here to Download",
                            data=response.content,
                            file_name="employees.pdf",
                            mime="application/pdf",
                        )
                        st.success("PDF generated successfully!")
                    else:
                        st.error("Failed to generate PDF")

        with tab3:
            st.subheader("Employee List")
            
            c1, c2 = st.columns(2)
            with c1:
                page = st.number_input("Pages", min_value=1)
            with c2:
                per_page = st.selectbox("Employees Per Page", options=[5, 10, 15, 20])

            params = {"page": int(page), "per_page": int(per_page)}
            get_url = f"{employee_url}/show_employee"

            if st.button("Show Employees"):
                response = requests.get(get_url, params=params)

                if response.status_code == 200:
                    raw_data = response.json()

                    if "Data" in raw_data:
                        employees = raw_data["Data"]
                        df = pd.DataFrame(employees)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.error("Server problem")

        with tab4:
            st.subheader("Search Employee")

            choice = st.selectbox("Menu:", options=["By ID", "By Name", "Salary Range"])
            
            if choice == "By ID":
                emp_id = st.number_input("Employee ID:", min_value=1, key="search_key")
                employee_search_url = f"{employee_url}/employee_by_id/{emp_id}"

                if st.button("Search"):
                    response = requests.get(employee_search_url)

                    if response.status_code == 200:
                        raw_data = response.json()

                        if "Data" in raw_data:
                            employee = raw_data["Data"]
                            df = pd.DataFrame([employee])
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.warning(f"Error: {response.json()}")
                
            elif choice == "By Name":
                pass
            
            elif choice == "Salary Range":
                col1, col2 = st.columns(2)

                with col1:
                    min_salary = st.number_input(
                        "Minimum Salary",
                        min_value=0.0,
                        step=1000.0
                    )

                with col2:
                    max_salary = st.number_input(
                        "Maximum Salary",
                        min_value=0.0,
                        step=1000.0
                    )

                if st.button("Search Employees"):
                    if min_salary > max_salary:
                        st.error("Minimum salary cannot be greater than maximum salary")

                    else:
                        try:
                            response = requests.get(
                                f"{employee_url}/filter_by_salary",
                                params={
                                    "min_salary": min_salary,
                                    "max_salary": max_salary
                                }
                            )

                            if response.status_code == 200:
                                result = response.json()
                                employees = result.get("Data", [])

                                if employees:
                                    st.success(f"{len(employees)} Employee(s) Found")
                                    df = pd.DataFrame(employees)
                                    st.dataframe(
                                        df,
                                        use_container_width=True,
                                        hide_index=True
                                    )
                                else:
                                    st.warning("No employees found in this salary range")
                            else:
                                st.error("Failed to fetch data")
                        except Exception as e:
                            st.error(str(e))

    elif choice == "Department":
        st.title("Department Management")
        
        department_url = f"{base_url}/department"
        tab1, tab2, tab3 = st.tabs(["Show All", "Manage", "Employees"])

        with tab1:
            show_url = f"{department_url}/show_department"
            response = requests.get(show_url)
            
            raw_data = response.json()
            
            if "Data" in raw_data:
                department = raw_data["Data"]
                df = pd.DataFrame(department)                                    
                st.dataframe(df,
                                use_container_width=True,
                                hide_index=True,
                                    column_config={
                                        "id": st.column_config.NumberColumn(
                                        "Department ID",
                                        width="small"
                                        ),
                                        "department": st.column_config.TextColumn(
                                        "Department Name",
                                        width="large"
                                        )
                                    }
                                )
                                
        with tab2:
            dept_choice = st.selectbox(
                "Operations:",
                ["select option here","Add Department", "Update Department", "Remove Department"],
            )

            if dept_choice == "Add Department":
                st.subheader("Add Department")
                name = st.text_input("name", key="dept_name")

                if st.button("Add Department"):
                    full_url = f"{department_url}/add_department"
                    response = requests.post(full_url, json={"name": name})

                    if response.status_code == 200:
                        st.success(f"{name}: Department Added")
                    else:
                        st.error("Server Error")
                        st.write(response.json())

            elif dept_choice == "Update Department":
                st.subheader("Update Information")

                dept_id = st.number_input("department ID", value=0)
                name = st.text_input("name")
                update_url = f"{department_url}/update_department/{dept_id}"

                if st.button("Update"):
                    response = requests.put(update_url, json={"name": name})

                    if response.status_code == 200:
                        st.success("Department updated")
                    else:
                        st.warning("something wrong")

            elif dept_choice == "Remove Department":
                st.subheader("Remove Department")

                dept_id = st.number_input(
                    "department id", 
                    min_value=1, 
                    key="remove_dept_key"
                )
                
                if "show_remove_section" not in st.session_state:
                    st.session_state.show_remove_section = False
                
                if "department_data" not in st.session_state:
                    st.session_state.department_data = None
                    
                fetch_dept = f"{base_url}/department/fetch_dept_id/{dept_id}"
                # delete_dept_url = f"{department_url}/delete_department/{dept_id}"    
                
                if st.button("remove"):
                    response = requests.get(fetch_dept)
                    
                    if response.status_code == 200:
                        raw_data = response.json()
                        # st.write(raw_data)
                        
                        if raw_data:
                            st.session_state.department_data = raw_data
                            st.session_state.show_remove_section = True
                        else:
                            st.error("Department not found")
                            
                if st.session_state.show_remove_section:
                    department = st.session_state.department_data
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_input("Department ID", value=department.get("ID", ""), disabled=True)
                    with c2:
                        st.text_input("Name", value=department.get("Name", ""), disabled=True)
                            
                    if st.button("Delete"):
                        delete_dept_url = (
                                            f"{department_url}/delete_department/{department['ID']}"
                                        )
                        result = requests.delete(delete_dept_url)
                        
                        if result.status_code == 200:
                            st.success("This Department is no longer Used")
                            st.session_state.show_remove_section = False
                            st.session_state.department_data = None
                        else:
                            st.warning("Server Error")
                            st.write(result.json())
                            
        with tab3:
            st.subheader("Department Dashboard")

            department_dashboard_url = f"{department_url}/employww_per_deptartment"
            response = requests.get(department_dashboard_url)

            if response.status_code == 200:
                data = response.json()
                departments = data["Data"]
                df = pd.DataFrame(departments)

                total_departments = len(df)
                total_employees = df["Employees"].sum()

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Departments", total_departments)
                with col2:
                    st.metric("Total Employees", total_employees)

                st.divider()

                st.subheader("Employees Per Department")
                chart_df = df.set_index("Department")
                st.bar_chart(chart_df["Employees"])

                st.divider()

                st.subheader("Department Details")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("Failed to load dashboard")

    elif choice == "Attendance":
        st.title("Attendance Tracker")
        
        try:
            response = requests.get(f"{base_url}/attendance/employees")
            result = response.json()
            employees = result.get("Data", [])
        except Exception as e:
            st.error(f"Failed to fetch employees: {e}")
            st.stop()

        if not employees:
            st.warning("No employees found")
            st.stop()

        header1, header2, header3, header4 = st.columns([1, 2, 2, 2])
        with header1:
            st.markdown("### ID")
        with header2:
            st.markdown("### Name")
        with header3:
            st.markdown("### Department")
        with header4:
            st.markdown("### Attendance")
        st.divider()

        attendance_records = []
        status_options = ["Present", "Absent", "Sick Leave", "Half Day"]

        with st.form("attendance_form"):
            
            for i, emp in enumerate(employees):
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                with col1:
                    st.write(emp["Id"])
                with col2:
                    st.write(emp["name"])
                with col3:
                    st.write(emp["department"])
                with col4:
                    status = st.selectbox(
                        "Select Status",
                        status_options,
                        key=f"attendance_{emp['Id']}_{i}",
                        label_visibility="collapsed",
                    )
                attendance_records.append({"employee_id": emp["Id"], "status": status})
            st.divider()

            submit = st.form_submit_button(
                "Submit Attendance", use_container_width=True
            )

        if submit:
            success_count = 0
            failed_count = 0
            
            try:
                for record in attendance_records:
                    response = requests.post(
                        f"{base_url}/attendance/mark",
                        json={"employee_id": record["employee_id"]},
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                    else:
                        failed_count += 1
                st.success(f"""
                    Attendance Submitted Successfully
                    Success: {success_count}
                    Failed: {failed_count}
                    """)
                st.balloons()
                st.rerun()

            except Exception as e:

                st.error(f"Failed to submit attendance: {e}")

    elif choice == "Salary":
        st.title("Salary Analysis")

        tab1, tab2, tab3 = st.tabs(["Generate Payroll", "View Payroll", "Yearly Bonus"])

        with tab1:
            st.markdown("### Generate Monthly Payroll")

            employee_id = st.number_input(
                "Enter Employee ID", min_value=1, step=1, key="generate_payroll"
            )

            if st.button("Generate Payroll", use_container_width=True):

                try:
                    response = requests.post(
                        f"{base_url}/payroll/generate/{employee_id}"
                    )
                    result = response.json()

                    if response.status_code in [200, 201]:
                        data = result.get("Data", {})
                        st.success(
                            result.get("Message", "Payroll generated successfully")
                        )

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Employee", data.get("Employee Name", "N/A"))
                            st.metric("Department", data.get("Department", "N/A"))
                            st.metric(
                                "Monthly Salary", f"₹ {data.get('Monthly Salary', 0)}"
                            )
                            st.metric(
                                "Attendance %",
                                f"{data.get('Attendance Percentage', 0)}%",
                            )

                        with col2:
                            st.metric("Present Days", data.get("Present Days", 0))
                            st.metric("Absent Days", data.get("Absent Days", 0))
                            st.metric("Half Days", data.get("Half Days", 0))
                            st.metric("Bonus", f"₹ {data.get( 'Bonus', 0)}")

                        st.divider()
                        st.metric("Final Salary", f"₹ {data.get('Final Salary', 0)}")
                        st.balloons()

                    else:
                        st.error(result.get("Message", "Failed to generate payroll"))

                except Exception as e:
                    st.error(str(e))

        with tab2:
            st.markdown("### View Employee Payroll")

            employee_id = st.number_input(
                "Enter Employee ID", min_value=1, step=1, key="view_payroll"
            )

            if st.button("Fetch Payroll", use_container_width=True):

                try:
                    response = requests.get(f"{base_url}/payroll/employee/{employee_id}")
                    result = response.json()

                    if response.status_code == 200:
                        data = result.get("Data", {})
                        st.success( result.get("Message", "Payroll fetched successfully") )
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("Employee", data.get("Employee Name", "N/A"))
                            st.metric("Department", data.get("Department", "N/A"))
                            st.metric("Month", data.get("Month", "N/A"))
                        with col2:
                            st.metric("Salary", f"₹ {data.get('Total Salary', 0)}")
                            st.metric( "Deduction", f"₹ {data.get('Total Deduction', 0)}" )
                            st.metric("Bonus", f"₹ {data.get('Bonus', 0)}")
                        st.divider()
                        st.metric("Final Salary", f"₹ {data.get('Final Salary', 0)}")
                        
                    else:
                        st.error(result.get("Message", "Payroll not found"))
                        
                except Exception as e:
                    st.error(str(e))

        with tab3:
            st.markdown("### Yearly Bonus Report")
            employee_id = st.number_input( "Enter Employee ID", min_value=1, step=1, key="yearly_bonus" )

            if st.button("Fetch Bonus Report", use_container_width=True):
                try:
                    response = requests.get( f"{base_url}/payroll/yearly_bonus/{employee_id}" )
                    result = response.json()

                    if response.status_code == 200:
                        data = result.get("Data", {})
                        st.success(result.get("Message", "Bonus report fetched"))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Employee", data.get("Employee Name", "N/A"))
                            st.metric("Department", data.get("Department", "N/A"))
                        with col2:
                            st.metric( "Total Yearly Bonus", f"₹ {data.get('Total Yearly Bonus', 0)}",)
                            st.metric( "Total Yearly Salary", f"₹ {data.get('Total Yearly Salary', 0)}",)
                        st.divider()

                        st.subheader("Monthly Payroll History")
                        monthly_reports = data.get("Monthly Reports", [])
                        
                        if monthly_reports:
                            df = pd.DataFrame(monthly_reports)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.warning("No payroll history found")

                    else:
                        st.error(result.get("Message", "Failed to fetch report"))

                except Exception as e:
                    st.error(str(e))

init_session()

if not st.session_state.authenticated:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        auth_page()
else:
    main_dashboard()
