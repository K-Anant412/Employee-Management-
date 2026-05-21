from DataBase.database import db
from datetime import datetime

class Attendance(db.Model):

    __tablename__ = "employee_attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    check_in = db.Column(
        db.DateTime,
        nullable=True
    )

    check_out = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    is_paid_leave = db.Column(
        db.Boolean,
        default=False
    )

    deduction_amount = db.Column(
        db.Float,
        default=0
    )