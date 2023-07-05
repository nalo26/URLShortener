from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from .models import Access

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["POST"])
def login():
    token = request.form.get("token", "")
    for access in Access.query.all():
        if check_password_hash(access.token, token):
            login_user(access)
            return redirect(url_for("main.index"))

    flash("Invalid token")
    return redirect(url_for("main.index"))
