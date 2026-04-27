import sys, os

from flask import Flask
from routes import auth_bp, main_bp, patients_bp, appointments_bp, schedule_bp

app = Flask(__name__)
app.secret_key = "meddoc-secret-2025"

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(schedule_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)