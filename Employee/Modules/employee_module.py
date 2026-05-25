from DataBase.database import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = "employees"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    salary = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable = False)
    
    attendances = db.relationship(
        "Attendance",
        backref="employee",
        cascade="all, delete-orphan"
    )