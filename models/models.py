from datetime import datetime


class Patient:
    def __init__(self, fio, birth_date, address, polis, snils):
        self.fio = fio
        self.birth_date = birth_date  # ДЕФЕКТ ТЗ: формат не задан
        self.address = address
        self.polis = polis            # ДЕФЕКТ ТЗ: длина/формат не указан
        self.snils = snils            # ДЕФЕКТ ТЗ: формат не задан
        self.emk: list["EMKEntry"] = []


class EMKEntry:
    def __init__(self, diagnosis, notes):
        self.diagnosis = diagnosis    # ДЕФЕКТ ТЗ: нет валидации кода МКБ-10
        self.notes = notes
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M")


class Doctor:
    def __init__(self, name, speciality):
        self.name = name
        self.speciality = speciality
        self.schedule: list[str] = []


class Appointment:
    def __init__(self, patient_fio, doctor_name, slot):
        self.patient_fio = patient_fio
        self.doctor_name = doctor_name
        self.slot = slot