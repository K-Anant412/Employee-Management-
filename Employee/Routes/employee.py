from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from Utils.Check_role import check_role
from Services.employee_service import (
    create_employee,
    search_emp_by_name,
    get_all_employees,
    get_emp_by_id,
    update_emp_by_id,
    delete_employee,
    get_emp_by_salary,
    sort_emp,
    emp_pdf,
    upload_emp,
    ui_show_employee,
)

employee_route = Namespace(
    "employees", description="show all employee's", path="/employee"
)
employee_model = employee_route.model(
    "Employee",
    {
        "name": fields.String(description="employee name"),
        "city": fields.String(description="employee city"),
        "email": fields.String(description="employee email"),
        "salary": fields.String(description="employee salary"),
        "department": fields.String(description="employee department"),
    },
)


@employee_route.route("/add_employee", methods=["POST"])  # add new employee__
class create_emp(Resource):
    @employee_route.expect(employee_model)
    def post(self):
        data = request.get_json()
        return create_employee(data)


@employee_route.route("/show_employee")  # show all employee's__
class show_employee(Resource):
    @employee_route.doc(
        params={
            "page": {"description": "Page number", "type": "int", "default": 1},
            "per_page": {
                "description": "Employees per page",
                "type": "int",
                "default": 4,
            },
        }
    )
    def get(self):

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        return get_all_employees(page=page, per_page=per_page)


@employee_route.route("/employee_sort/", methods=["GET"])  # sort employees by salary
class sort_employee(Resource):
    @employee_route.doc(
        params={
            "page": {"description": "Page number", "type": "int", "default": 1},
            "per_page": {
                "description": "Employees per page",
                "type": "int",
                "default": 5,
            },
        }
    )
    def get(self):

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        return sort_emp(page=page, per_page=per_page)


@employee_route.route("/search_by_name", methods=["GET"])
class SearchByName(Resource):
    @employee_route.doc(
        params={
            "name": "Employee name or part of the name to search for"
        }
    )
    def get(self):
        name = request.args.get("name", "").strip()
        
        if not name:
            return error_response("Name parameter is required", 400)
            
        return search_emp_by_name(name)


@employee_route.route("/employee_by_id/<int:id>")  # show employee by ID__
@employee_route.param("id")
class show_employee_by_id(Resource):
    def get(self, id):
        return get_emp_by_id(id)


@employee_route.route("/filter_by_salary")
class filter_salary(Resource):

    def get(self):

        min_salary = request.args.get("min_salary", type=float)
        max_salary = request.args.get("max_salary", type=float)

        return get_emp_by_salary(min_salary, max_salary)


@employee_route.route(
    "/update_employee/<int:id>", methods=["PUT"]
)  # update existing employee by ID__
class update_employee(Resource):
    @employee_route.param("id", "employee id", _in="path", required=True)
    @employee_route.expect(employee_model)
    # @check_role(["superadmin"])
    def put(self, id):
        data = request.get_json()
        return update_emp_by_id(id, data)


@employee_route.route(
    "/delete_employee/<int:id>", methods=["DELETE"]
)  # remove employee by ID__
class delete_emp(Resource):
    @employee_route.param("id", "Employee ID", _in="path", required=True)
    # @check_role(["superadmin"])
    def delete(self, id):
        return delete_employee(id)


@employee_route.route("/get_pdf_data")  # download employee data in PDF format
class get_file(Resource):
    def get(self):
        return emp_pdf()


parser = reqparse.RequestParser()
parser.add_argument("file", location="files", type=FileStorage, help="CSV file")


@employee_route.route("/get_data_csv")  # add multiple employees using CSV file
class upload_employee(Resource):
    @employee_route.expect(parser)
    def post(self):
        args = parser.parse_args()
        f = args["file"]
        return upload_emp(f)


@employee_route.route("/show_all_employees", methods=["GET"])
class show_all_employee(Resource):
    def get(self):
        return ui_show_employee()
