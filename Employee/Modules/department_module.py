from DataBase.database import db

class Department(db.Model):
    __tablename__ = "department"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    
    employees = db.relationship("Employee", backref="department")