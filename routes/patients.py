from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db
from routes.main import login_required

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patients_bp.route("/")
@login_required
def index():
    query = request.args.get("q", "").strip()
    pts = db.patients.search(query) if query else db.patients.all()
    return render_template("patients/index.html", patients=pts, query=query)


@patients_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        fio = request.form.get("fio", "").strip()
        if not fio:
            flash("ФИО обязательно", "error")
            return render_template("patients/form.html", patient=None)
        db.patients.register(
            fio,
            request.form.get("birth_date", "").strip(),
            request.form.get("address", "").strip(),
            request.form.get("polis", "").strip(),
            request.form.get("snils", "").strip(),
        )
        flash(f"Пациент «{fio}» зарегистрирован", "success")
        return redirect(url_for("patients.index"))
    return render_template("patients/form.html", patient=None)


@patients_bp.route("/<path:fio>/edit", methods=["GET", "POST"])
@login_required
def edit(fio):
    p = db.patients.patients.get(fio)
    if not p:
        flash("Пациент не найден", "error")
        return redirect(url_for("patients.index"))
    if request.method == "POST":
        db.patients.edit(fio,
            birth_date=request.form.get("birth_date"),
            address=request.form.get("address"),
            polis=request.form.get("polis"),
            snils=request.form.get("snils"),
        )
        flash("Данные обновлены", "success")
        return redirect(url_for("patients.index"))
    return render_template("patients/form.html", patient=p)


@patients_bp.route("/<path:fio>/delete", methods=["POST"])
@login_required
def delete(fio):
    db.patients.delete(fio)
    flash("Пациент удалён", "success")
    return redirect(url_for("patients.index"))


@patients_bp.route("/<path:fio>/emk", methods=["GET", "POST"])
@login_required
def emk(fio):
    p = db.patients.patients.get(fio)
    if not p:
        flash("Пациент не найден", "error")
        return redirect(url_for("patients.index"))
    if request.method == "POST":
        diagnosis = request.form.get("diagnosis", "").strip()
        notes = request.form.get("notes", "").strip()
        if not diagnosis:
            flash("Код диагноза обязателен", "error")
        else:
            db.emk.add_entry(fio, diagnosis, notes)
            flash("Запись добавлена в ЭМК", "success")
        return redirect(url_for("patients.emk", fio=fio))
    return render_template("patients/emk.html", patient=p)