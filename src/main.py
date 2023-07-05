from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    if current_user and current_user.is_authenticated:
        return render_template("index.html")
    return render_template("login.html")
