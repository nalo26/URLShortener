import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    db_url = "%s://%s:%s@%s:%s/%s" % (
        os.getenv("DB_ENGINE"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASS"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "views.index"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    from .database.models import Access

    @login_manager.user_loader
    def load_user(_id):
        return Access.query.get(int(_id))

    from .views import views as views_blueprint

    app.register_blueprint(views_blueprint)

    return app
