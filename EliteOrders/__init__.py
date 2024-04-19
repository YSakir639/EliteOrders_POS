
# Importing libraries for flask backend and sqlalchamy for managing models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Import the LoginManager class from the flask_login module
from flask_login import LoginManager

# Instantiating sqlalchamy class
db = SQLAlchemy()
# assingning the name of the database
DB_NAME = "database.db"  

# function to configure flask application and configure important settings
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "3$Yh9K|@w2Z*bN-"
    app.config["SQLALCHEMY_DATABASE_URI"]= f"sqlite:///{DB_NAME}"

    db.init_app(app)
    
    from .views import views
    from .auth import auth

# register blueprints with the app
    app.register_blueprint(auth,url_prefix="/")
    app.register_blueprint(views,url_prefix="/")

# import models from current directory
    from . import models
    with app.app_context():
        db.create_all()

        # Import the User model from the models module
    from .models import User

    # Initialize the LoginManager instance and configure the /login 
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Define a user_loader function for the LoginManager to load a user from the database
    @login_manager.user_loader
    def load_user(id):
        # Load the user from the database using the provided user ID
        return User.query.get((int(id)))


    return app

