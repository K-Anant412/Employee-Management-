import os
import requests
import streamlit as st

class APIClient:
    """
    Centralized HTTP API client for communicating with the Flask REST API.
    Handles base URL discovery (from st.secrets or ENV), session persistence,
    and unified response parsing.
    """
    def __init__(self):
        # Discover API Base URL: 
        # 1. Streamlit secrets (st.secrets["API_BASE_URL"])
        # 2. Environment variable API_BASE_URL
        # 3. Default fallback for local development
        default_url = "http://127.0.0.1:5001/api/v1"
        try:
            if "API_BASE_URL" in st.secrets:
                self.base_url = st.secrets["API_BASE_URL"].rstrip("/")
            else:
                self.base_url = os.getenv("API_BASE_URL", default_url).rstrip("/")
        except Exception:
            self.base_url = os.getenv("API_BASE_URL", default_url).rstrip("/")

        # Initialize session state for HTTP session persistence across Streamlit reruns
        if "http_session" not in st.session_state:
            st.session_state.http_session = requests.Session()
        self.session = st.session_state.http_session

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    def request(self, method: str, endpoint: str, **kwargs):
        """Generic wrapper around requests session with standard error handling."""
        url = self._url(endpoint)
        try:
            response = self.session.request(method, url, timeout=15, **kwargs)
            try:
                data = response.json()
            except Exception:
                data = {"Status": "Error", "Message": response.text or f"HTTP {response.status_code}"}
            return response.status_code, data
        except requests.exceptions.ConnectionError:
            return 503, {
                "Status": "Error",
                "Message": f"Unable to connect to Flask API backend at {self.base_url}. Please verify the server is running."
            }
        except requests.exceptions.Timeout:
            return 504, {"Status": "Error", "Message": "API request timed out. Please try again."}
        except Exception as e:
            return 500, {"Status": "Error", "Message": str(e)}

    # --- Auth Services ---
    def login(self, email, password):
        status, data = self.request("POST", "/auth/login", json={"email": email, "password": password})
        if status == 200 and data.get("Status") == "Success":
            st.session_state.authenticated = True
            st.session_state.user = data.get("Data", {})
        return status, data

    def register(self, user_name, email, password, role="employee"):
        payload = {
            "user_name": user_name,
            "email": email,
            "password": password,
            "role": role
        }
        return self.request("POST", "/auth/Register", json=payload)

    def change_password(self, email, password, new_password):
        payload = {
            "email": email,
            "password": password,
            "new_password": new_password
        }
        return self.request("PUT", "/auth/change_password", json=payload)

    def logout(self):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.http_session = requests.Session()

    # --- Employee Services ---
    def get_all_employees(self, page=1, per_page=50):
        return self.request("GET", f"/employee/show_employee?page={page}&per_page={per_page}")

    def get_employees_ui_all(self):
        return self.request("GET", "/employee/show_all_employees")

    def get_employee_by_id(self, emp_id):
        return self.request("GET", f"/employee/employee_by_id/{emp_id}")

    def search_employees_by_name(self, name):
        return self.request("GET", f"/employee/search_by_name?name={name}")

    def filter_employees_by_salary(self, min_sal, max_sal):
        return self.request("GET", f"/employee/filter_by_salary?min_salary={min_sal}&max_salary={max_sal}")

    def create_employee(self, name, city, email, salary, department):
        payload = {
            "name": name,
            "city": city,
            "email": email,
            "salary": str(salary),
            "department": department
        }
        return self.request("POST", "/employee/add_employee", json=payload)

    def update_employee(self, emp_id, data):
        return self.request("PUT", f"/employee/update_employee/{emp_id}", json=data)

    def delete_employee(self, emp_id):
        return self.request("DELETE", f"/employee/delete_employee/{emp_id}")

    def upload_employees_csv(self, file_bytes, filename="employees.csv"):
        files = {"file": (filename, file_bytes, "text/csv")}
        return self.request("POST", "/employee/get_data_csv", files=files)

    def download_employee_pdf(self):
        url = self._url("/employee/get_pdf_data")
        try:
            response = self.session.get(url, timeout=20)
            if response.status_code == 200:
                return response.content, None
            return None, f"Failed with status code {response.status_code}"
        except Exception as e:
            return None, str(e)

    # --- Department Services ---
    def get_departments(self):
        return self.request("GET", "/department/show_department")

    def get_departments_with_employee_counts(self):
        return self.request("GET", "/department/employww_per_deptartment")

    def create_department(self, name):
        return self.request("POST", "/department/add_department", json={"name": name})

    def update_department(self, dept_id, name):
        return self.request("PUT", f"/department/update_department/{dept_id}", json={"name": name})

    def delete_department(self, dept_id):
        return self.request("DELETE", f"/department/delete_department/{dept_id}")

    # --- Attendance Services ---
    def mark_attendance(self, emp_id):
        return self.request("POST", "/attendance/mark", json={"employee_id": emp_id})

    def get_attendance_employees(self):
        return self.request("GET", "/attendance/employees")

    def get_attendance_analysis(self, emp_id):
        return self.request("GET", f"/attendance/analysis/{emp_id}")

    # --- Payroll Services ---
    def generate_payroll(self, emp_id):
        return self.request("POST", f"/payroll/generate/{emp_id}")

    def get_employee_payroll(self, emp_id):
        return self.request("GET", f"/payroll/employee/{emp_id}")

    def get_yearly_bonus(self, emp_id):
        return self.request("GET", f"/payroll/yearly_bonus/{emp_id}")
