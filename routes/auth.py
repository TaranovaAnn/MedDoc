from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ok, role = db.auth.login(username, password)
        if ok:
            session["user"] = username
            session["role"] = role
            return redirect(url_for("main.index"))
        error = "Неверный логин или пароль"
    return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))