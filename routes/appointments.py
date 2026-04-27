from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from routes.main import login_required

appointments_bp = Blueprint("appointments", __name__, url_prefix="/appointments")


@appointments_bp.route("/")
@login_required
def index():
    apts = db.appointments.all()
    return render_template("appointments/index.html", appointments=apts)


@appointments_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        patient_fio = request.form.get("patient_fio", "").strip()
        doctor_name = request.form.get("doctor_name", "").strip()
        slot = request.form.get("slot", "").strip()
        ok, msg = db.appointments.book(patient_fio, doctor_name, slot)
        if ok:
            flash(f"Запись создана: {patient_fio} → {doctor_name} в {slot}", "success")
            return redirect(url_for("appointments.index"))
        flash(msg, "error")

    patients = db.patients.all()
    doctors = db.schedule.all_doctors()
    # Собираем свободные слоты по каждому врачу для JS
    free_slots = {d.name: db.appointments.free_slots(d.name) for d in doctors}
    return render_template("appointments/new.html",
                           patients=patients, doctors=doctors,
                           free_slots=free_slots)


# ─── Расписание ───────────────────────────────────────────────

schedule_bp = Blueprint("schedule", __name__, url_prefix="/schedule")


@schedule_bp.route("/")
@login_required
def index():
    doctors = db.schedule.all_doctors()
    booked = set((a.doctor_name, a.slot) for a in db.appointments.all())
    return render_template("schedule/index.html", doctors=doctors, booked=booked)


@schedule_bp.route("/add-doctor", methods=["POST"])
@login_required
def add_doctor():
    name = request.form.get("name", "").strip()
    spec = request.form.get("speciality", "").strip()
    if name:
        db.schedule.add_doctor(name, spec)
        flash(f"Врач «{name}» добавлен", "success")
    return redirect(url_for("schedule.index"))


@schedule_bp.route("/add-slot", methods=["POST"])
@login_required
def add_slot():
    doctor = request.form.get("doctor", "").strip()
    slot = request.form.get("slot", "").strip()
    # ДЕФЕКТ ТЗ: нет проверки формата слота и выходных дней
    if doctor and slot:
        db.schedule.add_slot(doctor, slot)
        flash(f"Слот {slot} добавлен врачу {doctor}", "success")
    return redirect(url_for("schedule.index"))