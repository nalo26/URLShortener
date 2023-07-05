from flask import Blueprint, render_template
from . import db

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("login.html")
