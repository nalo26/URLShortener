from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from database.models import Access, Level, Redirection

from . import db

views = Blueprint("views", __name__)


@views.route("/favicon.ico")
@views.route("/robots.txt")
def static_from_root():
    return redirect(url_for("static", filename=request.path[1:]))


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
        flash("You don't have permission to create redirection", "error")
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is not None:
        flash("Redirection with this name already exists", "error")
        return "Conflict", 409

    target = request.json.get("target")
    if target is None:
        flash("Target is required", "error")
        return "Bad Request", 400

    redirection = Redirection(source=path, target=target)
    db.session.add(redirection)
    db.session.commit()

    flash("Successfully created redirection", "success")
    return "OK", 200


@views.route("/<path:path>", methods=["POST"])
@login_required
def update_redirection(path):
    if current_user.level != Level.WRITE:
        flash("You don't have permission to update redirection", "error")
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is None:
        flash("Redirection does not exists", "error")
        return "Not Found", 404

    redirection.target = request.json.get("target", redirection.target)
    db.session.commit()

    flash("Successfully updated redirection", "success")
    return "OK", 200


@views.route("/<path:path>", methods=["DELETE"])
@login_required
def delete_redirection(path):
    if current_user.level != Level.WRITE:
        flash("You don't have permission to delete redirection", "error")
        return "Forbidden", 403

    redirection = Redirection.query.get(path)
    if redirection is None:
        flash("Redirection does not exists", "error")
        return "Not Found", 404

    db.session.delete(redirection)
    db.session.commit()

    flash("Successfully deleted redirection", "success")
    return "OK", 200


@views.context_processor
def processor():
    def format_url(url, size=50):
        if len(url) > size:
            return url[: size - 3] + "..."
        return url

    return dict(format_url=format_url)
