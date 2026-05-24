from DataBase.database import db
import pandas as pd
from Utils.Response import error_response, success_response
# from Utils.Check_role import check_superadmin
from Utils.Validation import employee_validation
from Modules.employee_module import Employee
from Modules.attendance_module import Attendance
from Modules.department_module import Department
from reportlab.platypus import SimpleDocTemplate, Table
from io import BytesIO
from flask import send_file, request

from io import BytesIO
from flask import send_file
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape

def create_employee(data):
    try:
        error = employee_validation(data)
        if error:
            return error_response("enter required information")
        dp = Department.query.filter_by(name=data["department"]).first()
        if not dp:
            return error_response("department not found", 400)
        employee = Employee(
                            name=data["name"], 
                            city=data["city"],
                            email=data["email"], 
                            salary=data["salary"], 
                            department_id=dp.id
                            )
        db.session.add(employee)
        db.session.commit()
        return success_response("employee added")
    except Exception as e :
        return error_response(str(e))

def get_all_employees(page=1, per_page=4):
    pag_obj = Employee.query.paginate(page=page, per_page=per_page, error_out=False)
    employee = Employee.query.all()
    employee = pag_obj.items
    
    result = []
    for emp in employee:
        result.append({
            "Id":emp.id,
            "name":emp.name,
            "city":emp.city,
            "email":emp.email,
            "salary":emp.salary,
            "department":emp.department.name if emp.department else "No Department"
        })
    return success_response("Employee fecthed", result)

def sort_emp(page=1, per_page=5):
    try:
        page_obj = Employee.query.order_by(Employee.salary).paginate(
                                            page=page, 
                                            per_page=per_page, 
                                            error_out=False
                                            )
        employee = page_obj.items
        data = []
        for emp in employee:
            data.append({
                "Id":emp.id,
                "name":emp.name,
                "salary":emp.salary,
                "department":emp.department_id if emp.department_id else None
            })
        return success_response("Employee fetched", data)
    except Exception as e:
        return error_response(str(e))
    
def search_emp_by_name(name):
    # Base query for Employee
    stmt = db.select(Employee).filter(Employee.name.like(f"%{name}%"))
    
    result = db.session.execute(stmt).scalars().all()
    
    if not result:
        return error_response(f"No employees found matching standard name: '{name}'", 404)
    
    output = []
    for item in result:
        output.append({
            "ID": item.id,
            "Name": item.name,
            "City": item.city,
            "Department": item.department.name if item.department else "No Department"
        })
        
    return success_response(message="Employees fetched successfully", data=output)
    
def get_emp_by_id(id):
    emp = db.session.get(Employee, id)
    if not emp:
        return error_response("Employee not found")
    result = {
        "name":emp.name,
        "email":emp.email,
        "salary":emp.salary,
        "city":emp.city,
        "department":emp.department.name if emp.department else "No employee found"
    }
    return success_response("Employee found", result)

def get_emp_by_salary(min_salary, max_salary):
    try:
        data = []
        employees = Employee.query.filter(
            Employee.salary >= min_salary,
            Employee.salary <= max_salary
        ).all()
        for emp in employees:
            data.append({
                "name": emp.name,
                "salary": emp.salary
            })
            
        return success_response("Employees", data)
    except Exception as e:
        return error_response(str(e))

def update_emp_by_id(id, data):
    try:
        emp = db.session.get(Employee, id)
        if not emp:
            return error_response("Employee not found")
        
        if "department" in data:
            dept = Department.query.filter_by(name=data["department"]).first()
            
            if not dept:
                return error_response("Department not found")
            emp.department_id = dept.id
            
        if "name" in data:
            emp.name = data["name"]
        if "email" in data:
            emp.email = data["email"]
        if "salary" in data:
            try:
                emp.salary = float(data["salary"])
            except:
                return error_response("Invalid salary format")
        db.session.commit()
        
        dept_name = None
        if emp.department_id:
            dept_obj = db.session.get(Department, emp.department_id)
            if dept_obj:
                dept_name = dept_obj.name

        result = {
            "name": emp.name,
            "email": emp.email,
            "salary": emp.salary,
            "department": dept_name # Use the manually fetched name
        }
        return success_response("employee updated", result)
        
    except Exception as e:
        print(e)
        return error_response(str(e))
    
def delete_employee(id):
    try:
        emp = db.session.get(Employee, id)

        if not emp:
            return error_response("Employee not found"), 404

        Attendance.query.filter_by(
            employee_id=id
        ).delete()

        db.session.delete(emp)
        db.session.commit()

        return success_response("Employee was deleted"), 200

    except Exception as e:
        db.session.rollback()

        print("DELETE ERROR:", e)

        return error_response(str(e), status_code=500)
    
def emp_pdf():
    try:
        buffer = BytesIO()
       
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph(
            "<b>Employee Management Report</b>",
            styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 20))

        employees = Employee.query.all()
        data = [[
            "ID",
            "Name",
            "City",
            "Email",
            "Salary",
            "Department"
        ]]

        for emp in employees:
            data.append([
                emp.id,
                emp.name,
                emp.city,
                emp.email,
                f"₹ {emp.salary}",
                emp.department.name if emp.department else "No Department"
            ])
        
        table = Table(data, colWidths=[40, 120, 100, 220, 90, 150])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ])

        for i in range(1, len(data)):
            if i % 2 == 0:
                bg_color = colors.lightgrey
            else:
                bg_color = colors.beige

            style.add(
                'BACKGROUND',
                (0, i),
                (-1, i),
                bg_color
            )

        table.setStyle(style)

        elements.append(table)

        doc.build(elements)

        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="employees.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return error_response(str(e))
    
def upload_emp(f):
    try:
        if not f:
            return error_response("File not found")
        
        df = pd.read_csv(f)
        
        employees = []
        
        for _, row in df.iterrows():
            emp = Employee(
                name = row["name"],
                email = row["email"],
                city = row["city"],
                department_id = row["department_id"],
                salary = row["salary"]
            )
            employees.append(emp)
            
        db.session.bulk_save_objects(employees)
        db.session.commit()
        
        return success_response("Employee's added")
    except Exception as e:
        return error_response(str(e))
    
def ui_show_employee():
    try:
        employees = Employee.query.all()

        data = []

        for emp in employees:
            data.append({
                "id": emp.id,
                "name": emp.name,
                "city": emp.city,
                "salary": emp.salary,
                "email": emp.email,
                "department": emp.department.name if emp.department else "N/A"
            })

        return success_response(
            "All employees fetched",
            data
        )
    except Exception as e:
        return error_response(str(e))