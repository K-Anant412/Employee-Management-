from flask import request
from flask_restx import ( Namespace, Resource, fields )

from Services.attendance_service import (
    mark_attendance,
    month_analysis,
    get_all_employees
)

attendance_route = Namespace(
                   "attendance",
                    description="Attendance APIs" 
                    )
attendance_model = attendance_route.model(
                   "Attendance",
                   { "employee_id": fields.Integer}
                   )

@attendance_route.route("/mark")
class MarkAttendance(Resource):
    
    @attendance_route.expect(attendance_model)
    def post(self):
        
            data = request.get_json()
            print(data)
            return mark_attendance(data)

@attendance_route.route("/employees")
class AttendanceEmployees(Resource):
    
    def get(self):
        return get_all_employees()

@attendance_route.route("/analysis/<int:id>")
class MonthlyAnalysis(Resource):
    
    def get(self, id):
        return month_analysis(id)