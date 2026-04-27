from .auth import auth_bp
from .main import main_bp
from .patients import patients_bp
from .appointments import appointments_bp, schedule_bp

__all__ = ["auth_bp", "main_bp", "patients_bp", "appointments_bp", "schedule_bp"]