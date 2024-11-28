from flask import Flask
from applications.config import LocalDevelopmentConfig
from applications.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)

    app.app_context().push()

    return app

app = create_app()
CORS(app,resources={r"/*": {"origins": "http://localhost:5173"}})


import applications.create_initial_data
import applications.routes

if __name__ == "__main__":
    app.run()