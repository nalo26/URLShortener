from flask import Blueprint
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["POST"])
def login():
    return "Login"
