from datetime import datetime, timedelta
import time
from threading import Thread
from Appointment.appointment_manager import AppointmentManager, Appointment, Reminder
from Websocket.WebsocketManager import WSServer
from RFID.rfid import RfidTrigger
from BLE.ble import BLE, check_BLE_is_ready, ConnectedState, ConnectingState, DisconnectedState
from buttonFileCount.btn_file_count import ButtonPressCounter
import json
from TTS.tts import TTS
from NLU.nlu import Nlu

# Configuration du serveur WebSocket
address = '192.168.1.16'
port = 8082
server = WSServer(address, port)

# Configuration du gestionnaire de rendez-vous
manager = AppointmentManager('/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/appointments.json')

# Configuration de la LED fade (à adapter selon votre utilisation)
led_fade_duration = 1  # Durée de la LED fade en secondes

base_time = time.time()  # Remplacez par votre temps de base
next_time = base_time
# Lancement du serveur dans un thread séparé
def run_server():
    server.start()
    try:
        while True:
            server.handle_clients()

            messages = server.get_received_messages()
            for message in messages:
                for client_socket in server.clients:  # Parcours des clients connectés
                    server.state.handle_message(server, message, client_socket,tts=Speaker,nlu=nlu,appointment=manager)  # Utilisation de client_socket
    except KeyboardInterrupt:
        server.stop()

nlu = Nlu()
nlu.fit()
server_thread = Thread(target=run_server)
server_thread.start()

rfid_trigger = RfidTrigger(numDevice=2)
ble_client = BLE()
button_press_counter = ButtonPressCounter("/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/button_press.json")
already_retrieved=False
firstLunch = True
firstLunchDelay = True
Speaker = TTS()
while True:
    
    rfid_trigger.read()  # This will run indefinitely
    card_state = rfid_trigger.get_state()

    if card_state and not ble_client.check_value_retrive():
        # Lancer le Bluetooth uniquement lorsque l'état de la carte passe à True
        print("Running BLE")
        # Connexion BLE
        ble_client.connect()

        while card_state and not ble_client.check_value_retrive():
            ble_client.check_connection()  # Vérifie la connexion BLE
            if ble_client.check_connection():
                received_message = ble_client.receive_message()
                if received_message is not None:
                    # Process the received message here
                    print("Received message:", received_message)
            else:
                ble_client.connect()

            rfid_trigger.read()
            card_state = rfid_trigger.get_state()
            
            btn_value = ble_client.check_btn_value()
            if btn_value and btn_value > 0:
                button_press_counter.update_button_press(btn_value)


        # Déconnexion BLE
        ble_client.disconnect()

    else:
        
        button_press_data = button_press_counter.read_data()
        if button_press_data:
            if button_press_data['count'] > 0:
                # server.send_to_all_clients('Whisper')
                pass
            current_time = datetime.now()  # Obtenir le temps actuel

        if time.time() > next_time:
            already_retrieved=False
            # Vérifier s'il y a un rappel à la temporalité actuelle
            current_appointment = manager.check_appointment(current_time)
            if current_appointment:
                print(f"Rappel : {current_appointment}")
                # Envoyer LED fade en WebSocket à tous les clients
                if server.get_led_status() == "Off_mode":
                    server.set_led_status("Fade_mode")
                    server.send_to_all_clients('Fade_mode')
            else:
                print(f"Aucun rappel prévu")

            # Vérifier les 10 prochaines minutes pour les rendez-vous
            for i in range(10):
                target_time = current_time + timedelta(minutes=i)
                appointment_exists = manager.check_appointment(target_time)
                if appointment_exists:
                    print(f"Rendez-vous prévu dans les 10 prochaines minutes : {appointment_exists}")
                    # Envoyer LED fade en WebSocket à tous les clients

                    if server.get_led_status() == "Off_mode":
                        server.set_led_status("Fade_mode")
                        server.send_to_all_clients('Fade_mode')
                        break  # Sortir de la boucle dès qu'un rendez-vous est trouvé

            # Mettre à jour le temps de base pour la prochaine itération
            base_time = time.time()

            # Attendre 1 minute avant la prochaine vérification
            next_time = base_time + 60
            
        

    # Vérifier la valeur du bouton
    btn_value = ble_client.check_btn_value()
    if btn_value and btn_value > 0:
        button_press_counter.update_button_press(btn_value)
    if ble_client.check_value_retrive():
        if firstLunch:
            server.set_led_status("Static_mode")
            Speaker.sound("Hub/TTS/Digital-bell.wav")
            startTime = time.time()
            firstLunch=False
        if time.time() - startTime > 1 and firstLunchDelay:
            server.set_led_status("Off_mode")
            # server.send_to_all_clients("Whisper")
            firstLunchDelay=False

    else : 
        firstLunch=True