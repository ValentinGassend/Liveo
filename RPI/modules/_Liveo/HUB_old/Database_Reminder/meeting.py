import json
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
class Meeting:
    def __init__(self, filename):
        self.filename = filename

    def add(self, new_data):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            new_data["id"] = len(file_data["rendezvous"]) + 1
            file_data["rendezvous"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def remove(self, info):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            for item in file_data["rendezvous"]:
                if info in item['titre']:
                    file_data["rendezvous"].remove(item)
                    break
        with open(self.filename, 'w') as f:
            json.dump(file_data, f, indent=2)

    def update(self, updated_data):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            for item in file_data["rendezvous"]:
                if item['id'] == len(file_data["rendezvous"]):
                    item.update(updated_data)
                    break
        with open(self.filename, 'w') as f:
            json.dump(file_data, f, indent=2)


    def check_current_date(self ):
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        with open(self.filename, 'r') as file:
            file_data = json.load(file)
            rendezvous = file_data["rendezvous"]
            for rdv in rendezvous:
                # ...
                rappel_date_str = rdv["rappel"]["date"]
                rappel_heure_str = rdv["rappel"]["heure"]
                rdv_date_str = rdv["date"]
                rdv_heure_str = rdv["heure"]

                rappel_date = datetime.strptime(rappel_date_str, "%Y-%m-%d").date() if rappel_date_str else None
                rappel_heure = datetime.strptime(rappel_heure_str, "%H:%M").time() if rappel_heure_str else None
                rdv_date = datetime.strptime(rdv_date_str, "%Y-%m-%d").date() if rdv_date_str else None
                rdv_heure = datetime.strptime(rdv_heure_str, "%H:%M").time() if rdv_heure_str else None

                if rappel_heure and rappel_date and rdv_heure and rdv_date:
                    if rappel_heure <= current_time <= rdv_heure and rappel_date == rdv_date == current_date:
                        print("Rappel pour le rendez-vous:", rdv["titre"])
                        return True

                elif rdv_date and rdv_date == current_date:
                    print("Rendez-vous aujourd'hui:", rdv["titre"])
                    return True

        return False
