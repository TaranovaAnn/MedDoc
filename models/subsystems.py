from .models import Patient, Doctor, Appointment, EMKEntry


class PatientSubsystem:
    def __init__(self):
        self.patients: dict[str, Patient] = {}

    def register(self, fio, birth_date, address, polis, snils) -> Patient:
        # ДЕФЕКТ ТЗ: поведение при дублировании ФИО не определено
        p = Patient(fio, birth_date, address, polis, snils)
        self.patients[fio] = p
        return p

    def edit(self, fio, **kwargs) -> Patient | None:
        p = self.patients.get(fio)
        if not p:
            return None
        for k, v in kwargs.items():
            if v:
                setattr(p, k, v)
        return p

    def delete(self, fio) -> bool:
        # ДЕФЕКТ ТЗ: судьба ЭМК при удалении пациента не определена
        return self.patients.pop(fio, None) is not None

    def search(self, query: str) -> list[Patient]:
        q = query.lower()
        return [p for p in self.patients.values() if q in p.fio.lower()]

    def all(self) -> list[Patient]:
        return list(self.patients.values())


class ScheduleSubsystem:
    def __init__(self):
        self.doctors: dict[str, Doctor] = {}

    def add_doctor(self, name, speciality) -> Doctor:
        d = Doctor(name, speciality)
        self.doctors[name] = d
        return d

    def add_slot(self, doctor_name, slot) -> bool:
        # ДЕФЕКТ ТЗ: формат слота не нормирован, выходные не проверяются
        d = self.doctors.get(doctor_name)
        if not d:
            return False
        d.schedule.append(slot)
        return True

    def all_doctors(self) -> list[Doctor]:
        return list(self.doctors.values())


class AppointmentSubsystem:
    def __init__(self, schedule: ScheduleSubsystem):
        self.appointments: list[Appointment] = []
        self._schedule = schedule

    def free_slots(self, doctor_name: str) -> list[str]:
        d = self._schedule.doctors.get(doctor_name)
        if not d:
            return []
        booked = {a.slot for a in self.appointments if a.doctor_name == doctor_name}
        return [s for s in d.schedule if s not in booked]

    def book(self, patient_fio, doctor_name, slot) -> tuple[bool, str]:
        if slot not in self.free_slots(doctor_name):
            return False, "Слот недоступен или уже занят"
        # ДЕФЕКТ ТЗ: не указано, нужно ли блокировать слот после записи
        self.appointments.append(Appointment(patient_fio, doctor_name, slot))
        return True, "Запись создана"

    def by_patient(self, fio: str) -> list[Appointment]:
        return [a for a in self.appointments if a.patient_fio == fio]

    def all(self) -> list[Appointment]:
        return self.appointments


class EMKSubsystem:
    def __init__(self, patients: PatientSubsystem):
        self._patients = patients

    def add_entry(self, fio, diagnosis, notes) -> EMKEntry | None:
        p = self._patients.patients.get(fio)
        if not p:
            return None
        # ДЕФЕКТ ТЗ: нет валидации кода МКБ-10
        entry = EMKEntry(diagnosis, notes)
        p.emk.append(entry)
        return entry


class AuthSubsystem:
    USERS = {
        "admin":   {"password": "admin123", "role": "Администратор"},
        "doctor1": {"password": "doc123",   "role": "Врач"},
        "reg1":    {"password": "reg123",   "role": "Регистратор"},
        "stat1":   {"password": "stat123",  "role": "Статистик"},
    }
    # ДЕФЕКТ ТЗ: нет требований к сложности пароля и блокировке после N попыток

    def login(self, username, password) -> tuple[bool, str | None]:
        u = self.USERS.get(username)
        if u and u["password"] == password:
            return True, u["role"]
        return False, None