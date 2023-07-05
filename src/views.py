from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash

from .models import Access

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    if current_user and current_user.is_authenticated:
        return render_template("index.html")

    # user not logged in
    return render_template("login.html")


@views.route("/", methods=["POST"])
def index_post():
    if current_user and current_user.is_authenticated:
        pass

    # user not logged in
    token = request.form.get("token", "")
    for access in Access.query.all():
        if check_password_hash(access.token, token):
            login_user(access)
            return redirect(url_for("views.index"))

    flash("Invalid token")
    return redirect(url_for("views.index"))
