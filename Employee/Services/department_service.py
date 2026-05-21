from DataBase.database import db
from Utils.Response import error_response, success_response
from Utils.Validation import department_validation
from Modules.department_module import Department
from Modules.employee_module import Employee
from sqlalchemy import func

def create_department(data):
    try:
        error = department_validation(data)
        if error:
            return error_response("enter department name")
        department = Department(name=data["name"])
        db.session.add(department)
        db.session.commit()
        result = {
            "id": department.id,
            "name": department.name
        }
        # return success_response("department was created" , result)
        return result
    except Exception as e:
        return error_response(str(e))
    
def show_all_department():
    try:
        data = Department.query.all()
        result = []
        for dep in data:
            result.append({
                "Id":dep.id,
                "Department": dep.name
            })
        return success_response("Departments", result)
    except Exception as e:
        return error_response(str(e))
    
def show_department_emp():
    try:
        data = db.session.query(
            Department.id,
            Department.name,
            func.count(Employee.id).label("employee_count")
        ).outerjoin(Employee, Department.id == Employee.department_id).group_by(Department.id).all()
        
        result = []
        
        for dep in data:
            result.append({
                "ID": dep.id,
                "Department": dep.name,
                "Employees": dep.employee_count
            })
        
        return success_response("Department with Employees", result)
    except Exception as e:
        return error_response(str(e))

def update_department(id, data):
    try:
        dep = Department.query.get(id)
        if not dep:
            return error_response("department not found")
        if "name" in data:
            dep.name = data["name"]
        return success_response("department was updated")
    except Exception as e:
        return error_response(str(e))

def delete_department(id):
    try:
        dep = Department.query.get(id)
        
        if not dep:
            return error_response("department not found")
        
        if dep.employees:
            return error_response(
                "Cannot delete department. Employees are assigned to it."
            )
        
        db.session.delete(dep)
        db.session.commit()
        
        return success_response("department was deleted") 
    except Exception as e:
        return error_response(str(e))
    
def fetch_department(id):
    try:
       dep = Department.query.get(id)
       if not dep:
           return error_response("department not found")
       result = {
           "ID": dep.id,
           "Name": dep.name
       }
       return result
    except Exception as e:
        return error_response(str(e))