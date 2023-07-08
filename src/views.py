from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from .models import Level, Access, Redirection
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    if not (current_user and current_user.is_authenticated):
        # user not logged in
        return render_template("login.html")

    # user logged in
    ctx = {
        "redirections": Redirection.query.order_by(Redirection.created_at.desc()).all(),
        "can_write": current_user.level == Level.WRITE,
    }
    return render_template("index.html", **ctx)


@views.route("/", methods=["POST"])
def login_logout():
    # user not logged in
    if not (current_user and current_user.is_authenticated):
        token = request.form.get("token", "")
        for access in Access.query.all():
            if check_password_hash(access.token, token):
                login_user(access)
                access.last_access = db.func.now()
                db.session.commit()
                return redirect(url_for("views.index"))

        flash("Invalid token", "error")
        return redirect(url_for("views.index"))

    # user logged in
    if request.json and request.json.get("method") == "logout":
        # logout
        logout_user()
        flash("Successfully logged out", "success")
        return "OK", 200

    return redirect(url_for("views.index"))


@views.route("/<path:path>", methods=["GET"])
def redirection(path):
    redirection = Redirection.query.get(path)
    if redirection is None:
        return render_template("404.html"), 404

    redirection.access_count += 1
    db.session.commit()
    return redirect(redirection.target)


@views.route("/<path:path>", methods=["PUT"])
@login_required
def create_redirection(path):
    if current_user.level != Level.WRITE:
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is not None:
        return "Conflict", 409

    target = request.json.get("target")
    if target is None:
        return "Bad Request", 400

    redirection = Redirection(source=path, target=target)
    db.session.add(redirection)
    db.session.commit()

    return "OK", 200


@views.route("/<path:path>", methods=["POST"])
@login_required
def update_redirection(path):
    if current_user.level != Level.WRITE:
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is None:
        return "Not Found", 404

    redirection.target = request.json.get("target", redirection.target)
    db.session.commit()

    return "OK", 200


@views.route("/<path:path>", methods=["DELETE"])
@login_required
def delete_redirection(path):
    if current_user.level != Level.WRITE:
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is None:
        return "Not Found", 404

    db.session.delete(redirection)
    db.session.commit()

    return "OK", 200
