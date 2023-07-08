from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash

from .models import Access, Redirection
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    if not (current_user and current_user.is_authenticated):
        # user not logged in
        return render_template("login.html")

    # user logged in
    ctx = {
        "redirections": Redirection.query.all(),
    }
    return render_template("index.html", **ctx)


@views.route("/", methods=["POST"])
def index_post():
    if not (current_user and current_user.is_authenticated):
        # user not logged in
        token = request.form.get("token", "")
        for access in Access.query.all():
            if check_password_hash(access.token, token):
                login_user(access)
                access.last_access = db.func.now()
                db.session.commit()
                return redirect(url_for("views.index"))

        flash("Invalid token")
        return redirect(url_for("views.index"))

    # user logged in
    # TODO: do things
    return redirect(url_for("views.index"))


@views.route("/<path:path>", methods=["GET"])
def redirection(path):
    redirection = Redirection.query.get(path)
    if redirection is None:
        return render_template("404.html"), 404

    redirection.access_count += 1
    db.session.commit()
    return redirect(redirection.target)
