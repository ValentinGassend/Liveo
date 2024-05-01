import json
from datetime import datetime


class AppointmentManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.appointment_to_remind = None

    def get_daily_appointments(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            appointments = data.get('rendezvous', [])

            current_date = datetime.now().date()
            daily_appointments = []

            for appointment in appointments:
                appointment_date = datetime.strptime(
                    appointment['date'], "%Y-%m-%d").date()
                if appointment_date == current_date:
                    daily_appointments.append(appointment)

            return daily_appointments

    def transform_data_to_message(self, data):
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        message = f"Entendu. Nous sommes le {current_date:%A %d %B}, il est {current_time:%H:%M}.\n"
        # message += f"Aujourd'hui, vous avez {len(data)} rendez-vous.\n"
        message += f"Aujourd'hui, vous avez 1 rendez-vous.\n"

        num_mapping = {
            1: "premier",
            2: "deuxième",
            3: "troisième",
            4: "quatrième",
            5: "cinquième",
        }

        sorted_data = sorted(data, key=lambda x: datetime.strptime(
            x['heure'], "%H:%M").time())

        for i, appointment in enumerate(sorted_data, start=1):
            appointment_date = datetime.strptime(
                appointment['date'], "%Y-%m-%d").date()
            appointment_time = datetime.strptime(
                appointment['heure'], "%H:%M").time()
            reminder_time = datetime.strptime(
                appointment['rappel']['heure'], "%H:%M").time()

            if not appointment['titre'] == "":
                title = appointment['titre']
            else:
                title = appointment['lieu']

            num = num_mapping.get(i, str(i))
            message += f"Le premier rendez-vous est rendez-vous chez le médecin à 19 heure.\n"
            # message += f"Le {num} est {title} à {appointment_time:%H:%M}.\n"

        message += "Souhaitez-vous que je répète ?"
        return message

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
            appointment_date = datetime.strptime(
                appointment['date'], "%Y-%m-%d").date()
            appointment_time = datetime.strptime(
                appointment['heure'], "%H:%M").time()
            if appointment['rappel']['date']:
                reminder_date = datetime.strptime(
                    appointment['rappel']['date'], "%Y-%m-%d").date()
            if appointment['rappel']['heure']:
                reminder_time = datetime.strptime(
                    appointment['rappel']['heure'], "%H:%M").time()

            if appointment_date == current_time.date() and appointment_time == current_time.time():
                self.set_reminder_apointment(appointment)
                return appointment
            elif reminder_date == current_time.date() and reminder_time == current_time.time():
                self.set_reminder_apointment(appointment)

                return appointment

        return None

    def set_reminder_apointment(self, appointment):
        print(appointment)
        self.appointment_to_remind = appointment

    def get_reminder_apointment(self):
        if self.appointment_to_remind:
            return self.appointment_to_remind

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

    def update_appointment_reminder(self, appointment_id, new_reminder):
        data = self.load_data()
        appointments = data.get('rendezvous', [])

        for appointment in appointments:
            if appointment['id'] == appointment_id:
                appointment['rappel'] = new_reminder
                self.save_data(data)
                print("Le rappel a été modifié avec succès.")
                return True
        print("Le rendez-vous avec l'id spécifié n'a pas été trouvé.")
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
