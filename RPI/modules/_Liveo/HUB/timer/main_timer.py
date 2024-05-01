from datetime import datetime, timedelta
import time
from Appointment.appointment_manager import AppointmentManager, Appointment, Reminder

base_time = time.time()  # Remplacez par votre temps de base

manager = AppointmentManager('/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/timer/appointments.json')

next_time = base_time 
while True:
    current_time = datetime.now()  # Obtenir le temps actuel

    if time.time() > next_time:
        # Vérifier s'il y a un rappel à la temporalité actuelle
        current_appointment = manager.check_appointment(current_time)
        if current_appointment:
            print(f"Rappel : {current_appointment}")
        else:
            print(f"Aucun rappel prévu")
            pass
        # Vérifier les 10 prochaines minutes pour les rendez-vous
        for i in range(10):
            target_time = current_time + timedelta(minutes=i)
            appointment_exists = manager.check_appointment(target_time)
            if appointment_exists:
                print(f"Rendez-vous prévu dans les 10 prochaines minutes : {appointment_exists}")
                break  # Sortir de la boucle dès qu'un rendez-vous est trouvé

        # Mettre à jour le temps de base pour la prochaine itération
        base_time = time.time()

        # Attendre 1 minute avant la prochaine vérification
    next_time = base_time + 60

