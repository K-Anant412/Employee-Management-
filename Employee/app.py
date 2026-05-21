from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from config import config
from DataBase.database import db

from Routes.auth_route import auth_routes
from Routes.employee import employee_route
from Routes.department import department_routes
from Routes.attendance import attendance_route
from Routes.payroll_route import payroll_route

from Services.mail_extension import mail
from Modules.employee_module import Employee
from Modules.attendance_module import Attendance


app = Flask(__name__)
CORS(app)
mail.init_app(app)

app.config.from_object(config) 
app.secret_key = "myProject123SessionKey"
db.init_app(app)

with app.app_context():
    db.create_all()
    
api = Api(
          app, 
          title="employee management API",
          description="a simple employee management API build with Flask", 
          doc="/swagger",
          prefix='/api/v1'
          ) 
api.add_namespace(auth_routes)  
api.add_namespace(employee_route)
api.add_namespace(department_routes)
api.add_namespace(attendance_route)
api.add_namespace(payroll_route)
     
if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)