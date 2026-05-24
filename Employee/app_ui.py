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


import streamlit as st

import streamlit as st

def auth_page():
    # 1. Custom CSS Injector for Layout and Scoping
    st.markdown("""
    <style>
    /* Global App Container Adjustment */
    .block-container {
        padding-top: 5rem;
        padding-bottom: 3rem;
        /* Let the main page expand naturally so tabs and titles breathe */
        max-width: 100% !important; 
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* ===== Title Header Stylings ===== */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        width: 100%;
    }
    
    .main-title {
        font-size: 36px; /* Slightly larger for emphasis */
        font-weight: 800;
        color: #1b2b42;
        letter-spacing: -1px;
        margin-bottom: 6px;
    }
    
    .subtitle {
        color: #5f7285;
        font-size: 16px;
        font-weight: 500;
    }

    /* ===== Tab Customizations ===== */
    /* Target the wrapper of the tabs to center them comfortably */
    .stTabs {
        width: 100% !important;
        max-width: 480px !important; /* Matches the form width perfectly */
        margin: 0 auto;
    }

    .stTabs [data-baseweb="tab-list"] {
        justify-content: center !important;
        gap: 16px !important;
        margin-bottom: 1.5rem !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 12px 36px !important; /* Wider tabs for easier clicking */
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background: #1b2b42 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(27, 43, 66, 0.15) !important;
    }

    /* ===== Glassmorphism Form Container ===== */
    /* Gives the login box a perfectly clear, standard desktop width */
    div[data-testid="stForm"] {
        width: 100% !important;
        max-width: 480px !important; /* Set to a highly readable standard login width */
        margin: 0 auto !important;
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05) !important;
    }

    /* ===== Input Field Fixes ===== */
    .stTextInput label, .stSelectbox label {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #1b2b42 !important;
        margin-bottom: 6px !important;
    }

    .stTextInput input, div[data-baseweb="select"] {
        height: 50px !important; /* Slightly taller for a premium feel */
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #1b2b42 !important;
        font-size: 15px !important;
    }
    
    .stTextInput input:focus, div[data-baseweb="select"]:focus-within {
        border-color: #1b2b42 !important;
        box-shadow: 0 0 0 1px #1b2b42 !important;
    }

    /* Form Inner Markdown Headings */
    .form-heading {
        font-size: 24px;
        font-weight: 700;
        color: #1b2b42;
        margin-bottom: 1.5rem;
    }

    /* ===== Unified Buttons ===== */
    .stButton > button, .stFormSubmitButton > button {
        width: 100% !important;
        height: 50px !important;
        border: none !important;
        border-radius: 12px !important;
        background: #1b2b42 !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(27, 43, 66, 0.2) !important;
        margin-top: 15px !important;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #243b5a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(27, 43, 66, 0.3) !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # 2. Header
    st.markdown("""
        <div class="header-container">
            <div class="main-title">Employee Management System</div>
            <div class="subtitle">Access your corporate dashboard portal</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])

    with tab1:
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="form-heading">Welcome Back</div>', unsafe_allow_html=True)

            email = st.text_input("Email Address", placeholder="name@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Sign In")

            if submit:
                 login_user(email, password)

    with tab2:
        with st.form("reg_form", clear_on_submit=False):
            st.markdown('<div class="form-heading">Create Account</div>', unsafe_allow_html=True)

            u_name = st.text_input("Full Name", placeholder="user")
            u_email = st.text_input("Work Email Address", placeholder="name@company.com")
            u_pass = st.text_input("Password", type="password", placeholder="Minimum 8 characters")
            u_role = st.selectbox("Organizational Role", ["Employee", "Admin", "Superadmin"])
            submit_reg = st.form_submit_button("Create Account")

            if submit_reg:
                register_user(u_name, u_email, u_pass, u_role)
                st.success("Registered!")


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
        
        employee_url = f"{base_url}/employee"
        tab1, tab2, tab3, tab4 = st.tabs(["Home", "Manage", "Employee List", "Search"])

        with tab1:
            BASE_URL = "http://127.0.0.1:5001/api/v1"

            st.title("Employee Dashboard")
            st.caption("Manage employees, analytics, reports, and departments.")

            response = requests.get(
                f"{BASE_URL}/employee/show_all_employees"
            )

            data = response.json()
            employees = data.get("Data", [])
            df = pd.DataFrame(employees)

            st.markdown("""
            <style>

            div[data-testid="stMetric"]{
                background: rgba(255,255,255,0.18);
                border: 1px solid rgba(255,255,255,0.25);
                padding: 20px;
                border-radius: 18px;
                backdrop-filter: blur(14px);
                box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
                text-align:center;
            }
            .chart-card{
                background: rgba(255,255,255,0.18);
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 22px;
                padding: 20px;
                backdrop-filter: blur(14px);
                box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
            }

            </style>
            """, unsafe_allow_html=True)

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
                    st.metric("Average Salary", f"₹ {avg_salary:,.0f}")

                with col4:
                    st.metric("Highest Salary", f"₹ {max_salary:,.0f}")

                st.markdown("<br>", unsafe_allow_html=True)


                col1, col2 = st.columns(2)
                with col1:

                    st.markdown(
                        '<div class="chart-card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Employee Distribution")

                    dept_data = df["department"].value_counts()

                    fig, ax = plt.subplots(figsize=(5.5, 4))

                    colors = [
                        "#0F4C81",
                        "#1D70A2",
                        "#2E86C1",
                        "#5DADE2",
                        "#85C1E9",
                        "#AED6F1"
                    ]

                    fig.patch.set_alpha(0)
                    ax.set_facecolor("none")

                    wedges, texts, autotexts = ax.pie(
                        dept_data,
                        labels=dept_data.index,
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                        wedgeprops={
                            "edgecolor": "white",
                            "linewidth": 1
                        },
                        textprops={
                            "fontsize": 12
                        }
                    )

                    ax.axis("equal")

                    st.pyplot(fig, use_container_width=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:

                    st.markdown(
                        '<div class="chart-card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Salary Distribution")

                    salary_data = (
                        df["salary"]
                        .astype(float)
                        .reset_index(drop=True)
                    )

                    fig, ax = plt.subplots(figsize=(6, 4))

                    fig.patch.set_alpha(0)
                    ax.set_facecolor("none")

                    ax.plot(
                        salary_data,
                        marker="o",
                        linewidth=2.5
                    )

                    ax.fill_between(
                        range(len(salary_data)),
                        salary_data,
                        alpha=0.2
                    )

                    ax.set_title(
                        "Employee Salaries",
                        fontsize=18,
                        pad=15
                    )

                    ax.set_xlabel("Employee Index")
                    ax.set_ylabel("Salary")

                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)

                    ax.grid(
                        alpha=0.25,
                        linestyle="--"
                    )

                    st.pyplot(fig, use_container_width=True)

                    st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.title("Employee Management")

            st.markdown("""
                    <style>

                    .glass-card{
                        background: rgba(255,255,255,0.15);
                        border: 1px solid rgba(255,255,255,0.25);
                        backdrop-filter: blur(18px);
                        border-radius: 26px;
                        padding: 30px;
                        box-shadow: 0px 8px 30px rgba(0,0,0,0.08);
                        margin-top: 15px;
                        margin-bottom: 20px;
                    }

                    div.stButton > button,
                    div.stDownloadButton > button,
                    div[data-testid="stFormSubmitButton"] button{

                        width: 100%;
                        border-radius: 14px;
                        height: 48px;

                        border: none;

                        background: rgba(255,255,255,0.7);
                        backdrop-filter: blur(12px);

                        font-weight: 600;
                        transition: 0.3s;
                    }

                    div.stButton > button:hover,
                    div.stDownloadButton > button:hover,
                    div[data-testid="stFormSubmitButton"] button:hover{
                        transform: translateY(-2px);
                    }

                    .stTextInput input,
                    .stNumberInput input{
                        border-radius: 14px !important;
                    }

                    .stSelectbox > div > div{
                        border-radius: 14px !important;
                    }

                    .section-title{
                        font-size: 26px;
                        font-weight: 600;
                        margin-bottom: 10px;
                    }

                    </style>
                    """, unsafe_allow_html=True)
            
            choice = st.selectbox(
                "select option here",
                options=[
                    "Add Employee",
                    "Update Employee",
                    "Remove Employee",
                    "Reports",
                ],
            )
            st.markdown('</div>', unsafe_allow_html=True)

            if choice == "Add Employee":

                st.markdown(
                    '<div class="glass-card">'
                    '<div class="section-title">'
                    'Add Employee'
                    '</div>',
                    unsafe_allow_html=True
                )

                with st.form("add_form"):

                    c1, c2 = st.columns(2)

                    with c1:
                        name = st.text_input(
                            "Name",
                            placeholder="Enter employee name"
                        )

                        city = st.text_input(
                            "City",
                            placeholder="Enter city"
                        )

                        salary = st.number_input(
                            "Salary",
                            min_value=0
                        )

                    with c2:
                        email = st.text_input(
                            "Email",
                            placeholder="example@gmail.com"
                        )

                        department = st.text_input(
                            "Department",
                            placeholder="HR / IT / Finance"
                        )

                    submit = st.form_submit_button(
                        "Add Employee"
                    )

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
                                f"{employee_url}/add_employee",
                                json=data
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Employee added successfully"
                                )
                            else:
                                st.error(
                                    "Failed to add employee"
                                )

                        except Exception as e:
                            st.error(
                                f"Server Error: {e}"
                            )

                st.markdown('</div>', unsafe_allow_html=True)
            
            elif choice == "Update Employee":

                st.markdown(
                    '<div class="glass-card">'
                    '<div class="section-title">'
                    'Update Employee'
                    '</div>',
                    unsafe_allow_html=True
                )

                emp_id = st.number_input(
                    "Employee ID",
                    min_value=1,
                    step=1
                )
    
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
                    
                    st.markdown(
                        "<hr>",
                        unsafe_allow_html=True
                    )

                    st.subheader("Employee Details")
                    
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
                            st.success("Employee information was Updated")
                            st.session_state.employee = params
                        else:
                            st.error(response.text)
            
            elif choice == "Remove Employee":
                
                st.markdown(
                    '<div class="glass-card">'
                    '<div class="section-title">'
                    'Remove Employee'
                    '</div>',
                    unsafe_allow_html=True
                )
                
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
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                    
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

                st.markdown(
                                """
                                <div class="glass-card">
                                    <div class="section-title">
                                        Employee Reports
                                    </div>
                                """,
                                unsafe_allow_html=True
                            )

                st.write(
                            "Generate employee reports in PDF format."
                        )            
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
            st.title("Employee List")

            if "employee_page" not in st.session_state:
                st.session_state.employee_page = 1

            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">
                        Browse Employees
                    </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns([1, 1, 2])

            with c1:
                per_page = st.selectbox(
                    "Employees Per Page",
                    options=[5, 10, 15, 20],
                    index=1
                )

            with c2:
                st.metric(
                    "Current Page",
                    st.session_state.employee_page
                )

            st.markdown("</div>", unsafe_allow_html=True)

            params = {
                "page": st.session_state.employee_page,
                "per_page": per_page
            }

            get_url = f"{employee_url}/show_employee"

            response = requests.get(
                get_url,
                params=params
            )

            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">
                        Employee Records
                    </div>
                """,
                unsafe_allow_html=True
            )

            if response.status_code == 200:

                raw_data = response.json()

                if "Data" in raw_data:

                    employees = raw_data["Data"]

                    if employees:

                        df = pd.DataFrame(employees)

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:
                        st.warning("No employees found.")

                else:
                    st.error("Server problem")

            else:
                st.error("Failed to fetch employees")

            st.markdown("</div>", unsafe_allow_html=True)

            prev_col, center_col, next_col = st.columns([1, 2, 1])

            with prev_col:
                if st.button(
                    "⬅ Previous",
                    use_container_width=True
                ):
                    if st.session_state.employee_page > 1:
                        st.session_state.employee_page -= 1
                        st.rerun()

            with center_col:
                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-size:20px;
                        font-weight:600;
                        padding-top:8px;
                    ">
                        Page {st.session_state.employee_page}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with next_col:
                if st.button(
                    "Next ➝",
                    use_container_width=True
                ):
                    st.session_state.employee_page += 1
                    st.rerun()

        with tab4:
                st.title("Search Employee")

                st.markdown("""
                <div class="glass-card">
                    <div class="section-title">
                        Search Options
                    </div>
                """, unsafe_allow_html=True)

                choice = st.selectbox(
                    "Search By",
                    options=[
                        "By ID",
                        "By Name",
                        "Salary Range"
                    ]
                )

                st.markdown("</div>", unsafe_allow_html=True)

                if choice == "By ID":

                    st.markdown("""
                    <div class="glass-card">
                        <div class="section-title">
                            Search Employee by ID
                        </div>
                    """, unsafe_allow_html=True)

                    emp_id = st.number_input(
                        "Employee ID",
                        min_value=1,
                        key="search_key"
                    )

                    employee_search_url = (
                        f"{employee_url}/employee_by_id/{emp_id}"
                    )

                    if st.button(
                        "Search Employee",
                        use_container_width=True
                    ):

                        response = requests.get(
                            employee_search_url
                        )

                        if response.status_code == 200:

                            raw_data = response.json()

                            if "Data" in raw_data:

                                employee = raw_data["Data"]

                                st.markdown("""
                                <div class="section-title">
                                    Search Result
                                </div>
                                """, unsafe_allow_html=True)

                                df = pd.DataFrame([employee])

                                st.dataframe(
                                    df,
                                    use_container_width=True,
                                    hide_index=True
                                )

                            else:
                                st.warning("Employee not found")

                        else:
                            st.error("Failed to fetch employee")

                    st.markdown("</div>", unsafe_allow_html=True)

                elif choice == "By Name":

                    st.markdown("""
                    <div class="glass-card">
                        <div class="section-title">
                            Search Employee by Name
                        </div>
                    """, unsafe_allow_html=True)

                    search_name = st.text_input(
                        "Employee Name",
                        placeholder="Enter employee name",
                        key="search_name_key"
                    ).strip()

                    employee_search_url = (
                        f"{employee_url}/search_by_name"
                    )

                    if st.button(
                        "Search Employee",
                        key="name_search_btn",
                        use_container_width=True
                    ):

                        if not search_name:
                            st.error(
                                "Please enter a name."
                            )

                        else:

                            response = requests.get(
                                employee_search_url,
                                params={
                                    "name": search_name
                                }
                            )

                            if response.status_code == 200:

                                raw_data = response.json()

                                if (
                                    "Data" in raw_data
                                    and raw_data["Data"]
                                ):

                                    employees_list = (
                                        raw_data["Data"]
                                    )

                                    st.success(
                                        f"{len(employees_list)} employee(s) found"
                                    )

                                    df = pd.DataFrame(
                                        employees_list
                                    )

                                    st.dataframe(
                                        df,
                                        use_container_width=True,
                                        hide_index=True
                                    )

                                else:
                                    st.warning(
                                        "No employee found"
                                    )

                            elif response.status_code == 404:
                                st.warning(
                                    "No employee found"
                                )

                            else:
                                try:
                                    error_msg = (
                                        response.json()
                                        .get(
                                            "Message",
                                            response.text
                                        )
                                    )
                                except Exception:
                                    error_msg = response.text

                                st.error(
                                    f"Error: {error_msg}"
                                )

                    st.markdown("</div>", unsafe_allow_html=True)

                elif choice == "Salary Range":

                    st.markdown("""
                    <div class="glass-card">
                        <div class="section-title">
                            Search by Salary Range
                        </div>
                    """, unsafe_allow_html=True)

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

                    if st.button(
                        "Search Employees",
                        use_container_width=True
                    ):

                        if min_salary > max_salary:

                            st.error(
                                "Minimum salary cannot be greater than maximum salary"
                            )

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

                                    employees = result.get(
                                        "Data",
                                        []
                                    )

                                    if employees:

                                        st.success(
                                            f"{len(employees)} employee(s) found"
                                        )

                                        df = pd.DataFrame(
                                            employees
                                        )

                                        st.dataframe(
                                            df,
                                            use_container_width=True,
                                            hide_index=True
                                        )

                                    else:
                                        st.warning(
                                            "No employees found in this range"
                                        )

                                else:
                                    st.error(
                                        "Failed to fetch data"
                                    )

                            except Exception as e:
                                st.error(str(e))

                    st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Department":
        st.title("Department Management")
        
        department_url = f"{base_url}/department"
        tab1, tab2, tab3 = st.tabs(["Employees", "Manage", "Show All"])

        with tab3:
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
            st.title("Department Management")

            st.markdown("""
                    <style>

                    .glass-card{
                        background: rgba(255,255,255,0.15);
                        border: 1px solid rgba(255,255,255,0.25);
                        backdrop-filter: blur(18px);
                        border-radius: 26px;
                        padding: 30px;
                        box-shadow: 0px 8px 30px rgba(0,0,0,0.08);
                        margin-top: 15px;
                        margin-bottom: 20px;
                    }

                    div.stButton > button,
                    div.stDownloadButton > button,
                    div[data-testid="stFormSubmitButton"] button{

                        width: 100%;
                        border-radius: 14px;
                        height: 48px;

                        border: none;

                        background: rgba(255,255,255,0.7);
                        backdrop-filter: blur(12px);

                        font-weight: 600;
                        transition: 0.3s;
                    }

                    div.stButton > button:hover,
                    div.stDownloadButton > button:hover,
                    div[data-testid="stFormSubmitButton"] button:hover{
                        transform: translateY(-2px);
                    }

                    .stTextInput input,
                    .stNumberInput input{
                        border-radius: 14px !important;
                    }

                    .stSelectbox > div > div{
                        border-radius: 14px !important;
                    }

                    .section-title{
                        font-size: 26px;
                        font-weight: 600;
                        margin-bottom: 10px;
                    }

                    </style>
                    """, unsafe_allow_html=True)

            dept_choice = st.selectbox(
                "Select Action",
                [
                    "Select Option",
                    "Add Department",
                    "Update Department",
                    "Remove Department"
                ]
            )

            st.markdown("</div>", unsafe_allow_html=True)

            if dept_choice == "Add Department":

                st.markdown("""
                <div class="glass-card">
                    <div class="section-title">
                        Add Department
                    </div>
                """, unsafe_allow_html=True)

                name = st.text_input(
                    "Department Name",
                    placeholder="Enter department name",
                    key="dept_name"
                )

                if st.button(
                    "Add Department",
                    use_container_width=True
                ):

                    full_url = (
                        f"{department_url}/add_department"
                    )

                    response = requests.post(
                        full_url,
                        json={"name": name}
                    )

                    if response.status_code == 200:
                        st.success(
                            f"{name} department added"
                        )
                    else:
                        st.error(
                            "Server Error"
                        )
                        st.write(
                            response.json()
                        )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            elif dept_choice == "Update Department":

                st.markdown("""
                <div class="glass-card">
                    <div class="section-title">
                        Update Department
                    </div>
                """, unsafe_allow_html=True)

                dept_id = st.number_input(
                    "Department ID",
                    min_value=1,
                    step=1
                )

                name = st.text_input(
                    "Department Name",
                    placeholder="Enter new department name"
                )

                update_url = (
                    f"{department_url}/update_department/{dept_id}"
                )

                if st.button(
                    "Update Department",
                    use_container_width=True
                ):

                    response = requests.put(
                        update_url,
                        json={"name": name}
                    )

                    if response.status_code == 200:
                        st.success(
                            "Department updated successfully"
                        )
                    else:
                        st.warning(
                            "Something went wrong"
                        )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            elif dept_choice == "Remove Department":

                st.markdown("""
                <div class="glass-card">
                    <div class="section-title">
                        Remove Department
                    </div>
                """, unsafe_allow_html=True)

                dept_id = st.number_input(
                    "Department ID",
                    min_value=1,
                    key="remove_dept_key"
                )

                if "show_remove_section" not in st.session_state:
                    st.session_state.show_remove_section = False

                if "department_data" not in st.session_state:
                    st.session_state.department_data = None

                fetch_dept = (
                    f"{base_url}/department/fetch_dept_id/{dept_id}"
                )

                if st.button(
                    "Fetch Department",
                    use_container_width=True
                ):

                    response = requests.get(
                        fetch_dept
                    )

                    if response.status_code == 200:

                        raw_data = response.json()

                        if raw_data:

                            st.session_state.department_data = raw_data
                            st.session_state.show_remove_section = True

                        else:
                            st.error(
                                "Department not found"
                            )

                if st.session_state.show_remove_section:

                    st.markdown("<hr>", unsafe_allow_html=True)

                    department = (
                        st.session_state.department_data
                    )

                    st.subheader(
                        "Department Details"
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        st.text_input(
                            "Department ID",
                            value=department.get(
                                "ID",
                                ""
                            ),
                            disabled=True
                        )

                    with c2:
                        st.text_input(
                            "Department Name",
                            value=department.get(
                                "Name",
                                ""
                            ),
                            disabled=True
                        )

                    if st.button(
                        "Delete Department",
                        use_container_width=True
                    ):

                        delete_dept_url = (
                            f"{department_url}/delete_department/"
                            f"{department['ID']}"
                        )

                        result = requests.delete(
                            delete_dept_url
                        )

                        if result.status_code == 200:

                            st.success(
                                "Department deleted successfully"
                            )

                            st.session_state.show_remove_section = False
                            st.session_state.department_data = None

                        else:
                            st.warning(
                                "Server Error"
                            )
                            st.write(
                                result.json()
                            )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )
                            
        with tab1:
            st.title("Department Dashboard")
            department_dashboard_url = (
                f"{department_url}/employww_per_deptartment"
            )

            response = requests.get(
                department_dashboard_url
            )
            st.markdown("""
            <style>
            
            div[data-testid="stMetric"]{
                background: rgba(255,255,255,0.18);
                border: 1px solid rgba(255,255,255,0.25);
                padding: 20px;
                border-radius: 18px;
                backdrop-filter: blur(14px);
                box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
                text-align:center;
            }
            
            </style>
                        """, unsafe_allow_html=True)
            
            if response.status_code == 200:

                data = response.json()
                departments = data["Data"]
                df = pd.DataFrame(departments)

                total_departments = len(df)
                total_employees = (
                    df["Employees"]
                    .astype(int)
                    .sum()
                )

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Total Departments",
                        total_departments
                    )

                with c2:
                    st.metric(
                        "Total Employees",
                        total_employees
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns([1.2, 1])

                with col1:

                    st.markdown("""
                    <div class="glass-card">
                        <div class="section-title">
                            Employees Per Department
                        </div>
                    """, unsafe_allow_html=True)

                    chart_df = (
                        df.set_index("Department")
                    )

                    fig, ax = plt.subplots(
                        figsize=(7, 4)
                    )

                    fig.patch.set_alpha(0)
                    ax.set_facecolor("none")

                    bars = ax.bar(
                        chart_df.index,
                        chart_df["Employees"]
                    )

                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)

                    ax.grid(
                        alpha=0.2,
                        linestyle="--"
                    )

                    ax.set_ylabel(
                        "Employees"
                    )

                    ax.set_xlabel(
                        "Department"
                    )

                    ax.tick_params(
                        axis="x",
                        rotation=20
                    )

                    st.pyplot(
                        fig,
                        use_container_width=True
                    )
                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )
                with col2:

                    st.markdown("""
                    <div class="glass-card">
                        <div class="section-title">
                            Department Details
                        </div>
                    """, unsafe_allow_html=True)

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

            else:
                st.error(
                    "Failed to load dashboard"
                )

    elif choice == "Attendance":

        st.title("Attendance Tracker")
        st.caption(
            "Manage daily employee attendance."
        )

        try:
            response = requests.get(
                f"{base_url}/attendance/employees"
            )

            result = response.json()
            employees = result.get(
                "Data",
                []
            )

        except Exception as e:
            st.error(
                f"Failed to fetch employees: {e}"
            )
            st.stop()

        if not employees:
            st.warning(
                "No employees found"
            )
            st.stop()

        status_options = [
            "Present",
            "Absent",
            "Sick Leave",
            "Half Day"
        ]

        attendance_records = []

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        # Header row
        h1, h2, h3, h4 = st.columns(
            [0.8, 2, 2, 2]
        )

        with h1:
            st.markdown("**ID**")

        with h2:
            st.markdown("**Employee Name**")

        with h3:
            st.markdown("**Department**")

        with h4:
            st.markdown("**Status**")

        st.divider()

        # ==========================
        # FORM
        # ==========================
        with st.form(
            "attendance_form"
        ):

            for i, emp in enumerate(
                employees
            ):

                c1, c2, c3, c4 = st.columns(
                    [0.8, 2, 2, 2]
                )

                with c1:
                    st.write(
                        emp["Id"]
                    )

                with c2:
                    st.write(
                        emp["name"]
                    )

                with c3:
                    st.write(
                        emp["department"]
                    )

                with c4:
                    status = st.selectbox(
                        "status",
                        status_options,
                        key=f"attendance_{i}",
                        label_visibility="collapsed"
                    )

                attendance_records.append({
                    "employee_id":
                    emp["Id"],

                    "status":
                    status
                })

            st.divider()

            submit = (
                st.form_submit_button(
                    "Submit Attendance",
                    use_container_width=True
                )
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        # ==========================
        # SUBMIT
        # ==========================
        if submit:

            success_count = 0
            failed_count = 0

            try:

                for record in attendance_records:

                    response = requests.post(
                        f"{base_url}/attendance/mark",
                        json={
                            "employee_id":
                            record[
                                "employee_id"
                            ],
                            "status":
                            record[
                                "status"
                            ]
                        }
                    )

                    if response.status_code in [
                        200,
                        201
                    ]:
                        success_count += 1
                    else:
                        failed_count += 1

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Submitted",
                        success_count
                    )

                with c2:
                    st.metric(
                        "Failed",
                        failed_count
                    )

                st.success(
                    "Attendance submitted successfully"
                )

            except Exception as e:
                st.error(str(e))

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
