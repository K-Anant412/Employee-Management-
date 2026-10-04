import os
from flask import Flask, jsonify
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

# Apply production configuration
app.config.from_object(config)
app.secret_key = app.config.get("SECRET_KEY", "prod-secure-ems-secret-key-2026")

# Configure CORS for cross-origin Streamlit Cloud requests
CORS(app, supports_credentials=True, origins="*")

mail.init_app(app)
db.init_app(app)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"[Warning] Database initialization warning: {e}")

# Health check route for cloud platform uptime monitoring (e.g. Render)
@app.route("/health", methods=["GET"])
@app.route("/api/v1/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "EMS Flask REST API",
        "version": "1.0.0"
    }), 200

api = Api(
    app,
    title="Employee Management API",
    description="REST API backend for the Employee Management System",
    doc="/swagger",
    prefix="/api/v1",
)

api.add_namespace(auth_routes)
api.add_namespace(employee_route)
api.add_namespace(department_routes)
api.add_namespace(attendance_route)
api.add_namespace(payroll_route)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)