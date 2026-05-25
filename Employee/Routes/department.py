from flask import request
from flask_restx import Namespace, Resource, fields
from Utils.Check_role import check_role

from Services.department_service import (
    create_department, 
    delete_department, 
    update_department, 
    show_all_department, 
    show_department_emp, 
    fetch_department
    )

department_routes = Namespace(
                    "department", 
                    description="creating department"
                    )
department_model = department_routes.model(
                   "Department",
                    {"name":fields.String(required=True, description="enter department name")}
                    )

@department_routes.route("/add_department")
class create_dep(Resource):

    @check_role(["superadmin"])
    @department_routes.expect(department_model)    
    def post(self):
        
        data = request.get_json()
        return create_department(data)
@department_routes.route("/show_department")
class show_dep(Resource):

    def get(self):
        return show_all_department()
@department_routes.route("/employww_per_deptartment")
class show_emp_dept(Resource):

    def get(self):
        
        return show_department_emp()

@department_routes.route("/update_department/<int:id>")
class update_dep(Resource):

    @department_routes.expect(department_model)
    @department_routes.param("id", "department_id", _in="path", required=True)
    def put(self, id):
        
        data = request.get_json()
        return update_department(id, data)
    
@department_routes.route("/fetch_dept_id/<int:id>")
class fetch_dept(Resource):

    @department_routes.param("id", "department_id", _in="path", required=True)
    def get(self, id):
        
        return fetch_department(id)
@department_routes.route("/delete_department/<int:id>", methods=["DELETE"])
class remove_dep(Resource):

    @department_routes.param("id", "department_id", _in="path", required=True)
    @check_role(["superadmin"])
    def delete(self, id):
        
        return delete_department(id)