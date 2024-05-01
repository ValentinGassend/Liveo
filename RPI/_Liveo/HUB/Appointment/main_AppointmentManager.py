from appointment_manager import AppointmentManager,Appointment, Reminder

file_path = '/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/Appointment/appointments.json'
manager = AppointmentManager(file_path)

appointments = manager.get_all_appointments()
for appointment in appointments:
    print(appointment)
print()

manager.reset_appointment_ids()

# Exemple d'utilisation pour lire tous les rendez-vous
appointments = manager.get_all_appointments()
for appointment in appointments:
    print(appointment)
print()

# Exemple d'utilisation pour récupérer un rendez-vous par ID
appointment_id = 2
appointment = manager.get_appointment_by_id(appointment_id)
if appointment:
    print(f"Rendez-vous avec ID {appointment_id}:")
    print(appointment)
else:
    print(f"Aucun rendez-vous trouvé avec ID {appointment_id}")
print()

# Exemple d'utilisation pour ajouter un nouveau rendez-vous avec un ID auto-incrémenté
new_appointment = Appointment(
    id=len(appointments)+1,  # Utilise le nombre de rendez-vous existants comme nouvel ID
    date="2023-06-10",
    heure="12:00",
    lieu="Salle de réunion C",
    titre="Réunion d'équipe",
    informations_supplementaires="Discussion des prochaines étapes du projet.",
    rappel=Reminder(date="2023-06-10", heure="11:30")
)
manager.add_appointment(new_appointment.to_dict())
print("Nouveau rendez-vous ajouté avec succès.")
print()

# Exemple d'utilisation pour mettre à jour un rendez-vous existant
appointment_id = 1
updated_data = {
    "lieu": "Salle de conférence A",
    "titre": "Présentation client (mise à jour)"
}
if manager.update_appointment(appointment_id, updated_data):
    print(f"Rendez-vous avec ID {appointment_id} mis à jour avec succès.")
else:
    print(f"Aucun rendez-vous trouvé avec ID {appointment_id}")
print()

# Exemple d'utilisation pour supprimer un rendez-vous existant
appointment_id = 1
if manager.delete_appointment(appointment_id):
    print(f"Rendez-vous avec ID {appointment_id} supprimé avec succès.")
    
    # Réorganiser les ID des rendez-vous restants
    for i in range(appointment_id + 1, len(appointments)):
        new_id = i - 1
        appointment_data = appointments[i]
        appointment_data["id"] = new_id
        manager.update_appointment(i, appointment_data)
        print(f"Rendez-vous avec ID {i} mis à jour avec l'ID {new_id}")
else:
    print(f"Aucun rendez-vous trouvé avec ID {appointment_id}")
print()


