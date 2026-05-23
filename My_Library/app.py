from flask import Flask, request
from flask_cors import CORS
from DataBase.database import db
from config import config
from flask_restx import Api

app = Flask(__name__)
CORS(app)

app.config.from_object(config)
app.secret_key = "mySecondProject123"
db.init_app(app)

with app.app_context():
    db.create_all()
    
api = Api(
          app, 
          title="library management API",
          description="a simple employee management API build with Flask", 
          doc="/swagger",
          prefix='/api/v1'
          ) 

if __name__ == "__main__":
    app.run(
            debug=True, 
            port=5001, 
            use_reloder=False
            )