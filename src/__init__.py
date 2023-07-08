import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")

    load_dotenv(".env")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.index"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    from .models import Access

    @login_manager.user_loader
    def load_user(_id):
        return Access.query.get(int(_id))

    from .views import views as views_blueprint

    app.register_blueprint(views_blueprint)

    return app
