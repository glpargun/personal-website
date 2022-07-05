from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app=Flask(__name__,template_folder='templates/')
    app.config['SECRET_KEY'] = 'gsdhajweu gda baasu'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    UPLOAD_FOLDER = "static/image/Upload/"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/admin/')


    from .models import User, Post, Like, About, Project, Contact, Visit
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.sign_in"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


