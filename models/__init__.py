from .models import Patient, Doctor, Appointment, EMKEntry
from .subsystems import (
    PatientSubsystem, ScheduleSubsystem, AppointmentSubsystem,
    EMKSubsystem, AuthSubsystem,
)


class MedDocSystem:
    def __init__(self):
        self.auth = AuthSubsystem()
        self.patients = PatientSubsystem()
        self.schedule = ScheduleSubsystem()
        self.appointments = AppointmentSubsystem(self.schedule)
        self.emk = EMKSubsystem(self.patients)
        self._seed()

    def _seed(self):
        self.schedule.add_doctor("Сидорова М.П.", "Терапевт")
        self.schedule.add_doctor("Козлов В.Н.", "Кардиолог")
        self.schedule.add_doctor("Иванченко А.С.", "Невролог")

        for slot in ["2025-12-01 09:00", "2025-12-01 09:30",
                     "2025-12-01 10:00", "2025-12-02 11:00"]:
            self.schedule.add_slot("Сидорова М.П.", slot)
        for slot in ["2025-12-01 14:00", "2025-12-03 09:00"]:
            self.schedule.add_slot("Козлов В.Н.", slot)
        for slot in ["2025-12-02 10:00", "2025-12-04 15:00"]:
            self.schedule.add_slot("Иванченко А.С.", slot)

        p = self.patients.register(
            "Петрова Мария Сергеевна", "15.03.1985",
            "г. Москва, ул. Садовая, д. 12, кв. 5",
            "7894561230987654", "234-567-890 11",
        )
        self.emk.add_entry(p.fio, "J06.9",
                           "ОРВИ, лёгкое течение. Назначен постельный режим.")
        self.emk.add_entry(p.fio, "K29.1",
                           "Острый гастрит. Назначена диета №1.")

        self.patients.register(
            "Иванов Алексей Петрович", "20.07.1972",
            "г. Москва, пр. Мира, д. 45",
            "1234567890123456", "123-456-789 00",
        )


db = MedDocSystem()

__all__ = ["db", "Patient", "Doctor", "Appointment", "EMKEntry",
           "PatientSubsystem", "ScheduleSubsystem", "AppointmentSubsystem",
           "EMKSubsystem", "AuthSubsystem"]