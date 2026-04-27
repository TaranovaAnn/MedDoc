from flask import Blueprint, render_template, session, redirect, url_for
from models import db

main_bp = Blueprint("main", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@main_bp.route("/dashboard")
@login_required
def index():
    pts = db.patients.all()
    apts = db.appointments.all()
    doctors = db.schedule.all_doctors()
    total_emk = sum(len(p.emk) for p in pts)
    # Нагрузка врачей для мини-отчёта
    load = {}
    for a in apts:
        load[a.doctor_name] = load.get(a.doctor_name, 0) + 1
    return render_template("dashboard.html",
                           patients=pts, appointments=apts,
                           doctors=doctors, total_emk=total_emk,
                           doctor_load=load)