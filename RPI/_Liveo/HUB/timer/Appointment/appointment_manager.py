import json
from datetime import datetime
class AppointmentManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            return data

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def get_all_appointments(self):
        data = self.load_data()
        return data.get('rendezvous', [])

    def check_appointment(self, current_time):
        appointments = self.get_all_appointments()
        for appointment in appointments:
            appointment_date = datetime.strptime(appointment['date'], "%Y-%m-%d").date()
            appointment_time = datetime.strptime(appointment['heure'], "%H:%M")
            reminder_date = datetime.strptime(appointment['rappel']['date'], "%Y-%m-%d").date()
            reminder_time = datetime.strptime(appointment['rappel']['heure'], "%H:%M")

            if appointment_date == current_time.date() and appointment_time.strftime("%H:%M") == current_time.time().strftime("%H:%M"):
                return appointment
            elif reminder_date == current_time.date() and reminder_time.strftime("%H:%M") == current_time.time().strftime("%H:%M"):
                return appointment

        return None

    def get_appointment_by_id(self, appointment_id):
        appointments = self.get_all_appointments()
        for appointment in appointments:
            if appointment['id'] == appointment_id:
                return appointment
        return None

    def add_appointment(self, appointment):
        data = self.load_data()
        appointments = data.get('rendezvous', [])
        appointments.append(appointment)
        self.save_data(data)

    def update_appointment(self, appointment_id, updated_data):
        data = self.load_data()
        appointments = data.get('rendezvous', [])
        for appointment in appointments:
            if appointment['id'] == appointment_id:
                appointment.update(updated_data)
                self.save_data(data)
                return True
        return False

    def delete_appointment(self, appointment_id):
        data = self.load_data()
        appointments = data.get('rendezvous', [])
        for appointment in appointments:
            if appointment['id'] == appointment_id:
                appointments.remove(appointment)
                self.save_data(data)
                return True
        return False

    def reset_appointment_ids(self):
        data = self.load_data()
        appointments = data.get('rendezvous', [])

        for i, appointment in enumerate(appointments):
            appointment['id'] = i

        self.save_data(data)
        print("Les ID des rendez-vous ont été réinitialisés avec succès.")
class Appointment:
    def __init__(self, id, date, heure, lieu="", titre="", informations_supplementaires="", rappel=None):
        self.id = id
        self.date = date
        self.heure = heure
        self.lieu = lieu
        self.titre = titre
        self.informations_supplementaires = informations_supplementaires
        self.rappel = rappel
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "heure": self.heure,
            "lieu": self.lieu,
            "titre": self.titre,
            "informations_supplementaires": self.informations_supplementaires,
            "rappel": self.rappel.to_dict() if self.rappel else None
        }
    
class Reminder:
    def __init__(self, date, heure):
        self.date = date
        self.heure = heure
    
    def to_dict(self):
        return {
            "date": self.date,
            "heure": self.heure
        }