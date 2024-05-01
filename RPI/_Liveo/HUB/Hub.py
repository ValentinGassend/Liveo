from datetime import datetime, timedelta
import time
from threading import Thread
from Appointment.appointment_manager import AppointmentManager, Appointment, Reminder
from Websocket.WebsocketManager import WSServer
from RFID.rfid import RfidTrigger
from BLE.ble import BLE, check_BLE_is_ready
from buttonFileCount.btn_file_count import ButtonPressCounter
from WebServer.webserver import WebServer
from WebServer.webclient import WebSocketClient
import multiprocessing
import json
import subprocess
from btn.btn import Btn
from TTS.tts import TTS
from NLU.nlu import Nlu
import threading
import locale
address = '192.168.43.242'
# address = '192.168.1.16'
port = 8081
webport = 3000
server = WSServer(address, port)
myWebServeur = WebServer(address, webport)

server_process = multiprocessing.Process(target=myWebServeur.start)
server_process.start()

client = WebSocketClient('http://'+address+':'+str(webport)+'/')
client.connect()
# Configuration du gestionnaire de rendez-vous
manager = AppointmentManager(
    '/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/appointments.json')
manager.reset_appointment_ids()
# Configuration de la LED fade (à adapter selon votre utilisation)
led_fade_duration = 1  # Durée de la LED fade en secondes
button_pin = 10
my_btn = Btn(button_pin)
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
                    # Utilisation de client_socket
                    server.state.handle_message(
                        server, message, client_socket)
                    hub.handle_message(message)
    except KeyboardInterrupt:
        server.stop()


rfid_trigger = RfidTrigger(numDevice=2)
ble_client = BLE()
button_press_counter = ButtonPressCounter(
    "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/button_press.json")
already_retrieved = False
firstLunch = True
firstLunchDelay = True
Speaker = TTS()

nlu = Nlu()

server_thread = Thread(target=run_server)
server_thread.start()
print("server is ready")


chromium_command = "chromium-browser --kiosk http://192.168.43.242:3000"
subprocess.Popen(chromium_command, shell=True)
# Classe de base pour les états du hub


class HubState:
    def __init__(self):
        self.message = None
        self.previous_message = None

    def handle_message(self, hub, message):
        if not message == "PING":
            print("Message reçu dans Handle:", message)
        self.message = message

    def get_received_message(self):
        print("message", self.message)
        return self.message

    def handle_rfid_trigger(self, hub):
        pass

    def handle_button_trigger(self, hub):
        pass

    def handle_reminder(self, hub):
        pass

    def handle_self_state(self, hub):
        print("Erreur : Impossible de rester dans l'état actuel")

    def send_web_message(self, message):
        if client.isConnected():
            # Vous pouvez placer d'autres actions ici avant d'envoyer un message
            client.send_message(message)


# Implémentation de l'état de veille
class StandbyState(HubState):
    def handle_rfid_trigger(self, hub):
        print(f"Changement d'état : Veille -> Récupération d'information")
        hub.set_state(RecoveryState())

    def handle_button_trigger(self, hub):
        print(f"Changement d'état : Veille -> Déclenchement de bouton")
        hub.set_state(ButtonTriggerState())

    def handle_reminder(self, hub):
        print(f"Changement d'état : Veille -> Mode rappel")
        hub.set_state(ReminderModeState())

    def handle_standby(self, hub):
        print("Erreur : Impossible de rester dans l'état actuel")

    def handle_self_state(self, hub):
        pass

    def send_message_via_websocket(self, hub, message):
        # Code pour envoyer un message via WebSocket
        server.send_to_all_clients(message)


class TestState(HubState):
    def __init__(self):
        self.message = None
        self.led = False
        self.pc = False
        self.previous_message = None

    def handle_rfid_trigger(self, hub):
        pass

    def handle_button_trigger(self, hub):
        pass

    def handle_reminder(self, hub):
        pass

    def handle_standby(self, hub):
        hub.set_state(StandbyState())

    def handle_self_state(self, hub):
        pass

    def communicate_via_websocket(self, hub, expected_message=None):
        # Code pour communiquer via WebSocket
        received_message = None

        def wait_for_message():
            nonlocal received_message
            received_message = hub.get_received_message()

            # Vérifier si un message est déjà disponible
        wait_thread = threading.Thread(target=wait_for_message)
        wait_thread.start()
        wait_thread.join(timeout=0)  # Ne pas attendre le thread

        return received_message

    def send_message_via_websocket(self, hub, message):
        # Code pour envoyer un message via WebSocket
        server.send_to_all_clients(message)

    def websocket_connexion(self, hub):
        hub.send_message_via_websocket('ID')
        received_message = self.get_received_message()
        print("message: " + received_message)
        if received_message == "LED" and not self.led:
            self.led = True
            print("LED is connected !")
        if received_message == "PC" and not self.pc:
            self.pc = True
            print("Whisper support is connected !")
        if self.pc and self.led:
            return True
        elif self.pc:
            print("Whisper support is connected ! Led remain")
            return False
        elif self.led:
            print("LED is connected ! Whisper support remain")
            return False
        else:
            print(
                "You have to connect your leds and your Whisper support ! See you in 1s :)")
            return False


# Implémentation de l'état de récupération d'information
class RecoveryState(HubState):
    def __init__(self):
        self.message = None
        self.bluetooth_connected = False
        self.previous_message = None

    def handle_rfid_trigger(self, hub):
        print("Erreur : Impossible de rester dans l'état actuel")

    def handle_button_trigger(self, hub):
        pass

    def handle_reminder(self, hub):
        pass

    def handle_standby(self, hub):
        hub.set_state(StandbyState())

    def handle_self_state(self, hub):
        pass

    def launch_bluetooth(self, hub):
        # Code pour lancer le Bluetooth
        # ble_client.connect()
        self.bluetooth_connected = ble_client.is_connected()
        while not self.bluetooth_connected:
            ble_client.connect()
            self.bluetooth_connected = ble_client.is_connected()

    def communicate_with_ble(self, hub):
        if self.bluetooth_connected:
            # Code pour communiquer avec le BLE
            ble_client.connect()
            while True:
                received_message = ble_client.receive_message()
                # Code pour vérifier si une valeur est récupérée du BLE
                if received_message:
                    if ble_client.handle_message(received_message):
                        ble_client.disconnect()
                        print(ble_client.get_btn_value())
                        return ble_client.get_btn_value()

    def communicate_via_websocket(self, hub, expected_message=None):
        # Code pour communiquer via WebSocket
        received_message = None

        def wait_for_message():
            nonlocal received_message
            server.handle_clients()

            received_message = hub.get_received_message()
        # Attendre la réception d'un message
        while received_message is None:
            wait_thread = threading.Thread(target=wait_for_message)
            wait_thread.start()
            wait_thread.join()

        return received_message

    def send_message_via_websocket(self, hub, message):
        # Code pour envoyer un message via WebSocket
        server.send_to_all_clients(message)

    def update_json(self, hub, data):
        # Code pour ajouter, modifier ou mettre à jour des informations dans un JSON
        # Utilisez la bibliothèque JSON pour effectuer les opérations sur le JSON
        pass

    def add_appointment(self, hub, data, intent):
        if intent == "rdv":
            json_data = {
                "id": 0,
                "date": "",
                "heure": "",
                "lieu": "",
                "titre": "",
                "informations_supplementaires": "",
                "rappel": {
                        "date": "",
                        "heure": ""
                }
            }
            for slot in data['slots']:
                if slot['slotName'] == 'date':
                    date_value = slot['value']['value']
                    date_parsed = datetime.strptime(
                        date_value, "%Y-%m-%d %H:%M:%S %z")
                    json_data['date'] = date_parsed.strftime(
                        "%Y-%m-%d")
                elif slot['slotName'] == 'heure':
                    heure_value = slot['value']['value']
                    heure_parsed = datetime.strptime(
                        heure_value, "%Y-%m-%d %H:%M:%S %z")
                    json_data['heure'] = heure_parsed.strftime(
                        "%H:%M")
                elif slot['slotName'] == 'lieu':
                    json_data['lieu'] = slot['value']['value']
                elif slot['slotName'] == 'type_rendez_vous':
                    json_data['titre'] = slot['value']['value']
                elif slot['slotName'] == 'informations_supplementaires':
                    json_data['informations_supplementaires'] = slot['value']['value']
            json_data['id'] = -1
            print(json_data)
            manager.add_appointment(json_data)
            return json_data
        pass

    def update_appointment_reminder(self, hub, data, intent):
        if intent == "remind":
            json_data_remind = {
                "id": 0,
                "date": "",
                "heure": "",
                "lieu": "",
                "titre": "",
                "informations_supplementaires": "",
                "rappel": {
                        "date": "",
                        "heure": ""
                }
            }

            for slot in data['slots']:
                if slot['slotName'] == 'date':
                    date_value = slot['value']['value']
                    date_parsed = datetime.strptime(
                        date_value, "%Y-%m-%d %H:%M:%S %z")
                    json_data_remind["rappel"]["date"] = date_parsed.strftime(
                        "%Y-%m-%d")
                elif slot['slotName'] == 'time':
                    heure_value = slot['value']['value']
                    heure_parsed = datetime.strptime(
                        heure_value, "%Y-%m-%d %H:%M:%S %z")
                    json_data_remind["rappel"]["heure"] = heure_parsed.strftime(
                        "%H:%M")
            json_data_remind['id'] = -1
            print(json_data_remind)
            manager.update_appointment_reminder(
                json_data_remind['id'], json_data_remind["rappel"])
            return json_data_remind
        pass

    def launch_tts(self, hub, file):
        # Lancement du TTS en mode lecture de fichier audio
        Speaker.sound(file)

    def speak_text(self, hub, text):
        # Lancement du TTS en mode lecture de texte
        Speaker.talk(text)

    def run_nlu(self, hub, text, intent):
        if intent == "rdv":
            nlu_rdv = nlu.run(text=text, intent=intent)
            intent_name = nlu_rdv['intent']['intentName']
            if intent_name == None:
                return intent_name
            else:
                return nlu_rdv
        elif intent == "bool":
            nlu_bool = nlu.run(text=text, intent=intent)
            intent_name = nlu_bool['intent']['intentName']
            if intent_name == None:
                return False
            else:
                return intent_name
        elif intent == "remind":
            nlu_remind = nlu.run(text=text, intent=intent)
            intent_name = nlu_remind['intent']['intentName']
            if intent_name == None:
                return intent_name
            else:
                return nlu_remind


# Implémentation de l'état de déclenchement de bouton
class ButtonTriggerState(HubState):

    def handle_reminder(self, hub):
        print("Erreur : Impossible de passer en mode rappel en dehors de l'état de veille")

    def handle_standby(self, hub):
        hub.set_state(StandbyState())

    def handle_button_trigger(self, hub):
        print("Erreur : Impossible de rester dans l'état de déclenchement de bouton")

    def launch_tts(self, hub, file):
        # Lancement du TTS en mode lecture de fichier audio
        Speaker.sound(file)

    def speak_text(self, hub, text):
        # Lancement du TTS en mode lecture de texte
        Speaker.talk(text)

    def send_message_via_websocket(self, hub, message):
        # Code pour envoyer un message via WebSocket
        server.send_to_all_clients(message)

    def run_nlu(self, hub, text, intent):
        if intent == "choice":
            nlu_choice = nlu.run(text=text, intent=intent)
            print(nlu_choice)
            intent_name = nlu_choice['intent']['intentName']
            if intent_name == None:
                return False
            else:
                return intent_name
        elif intent == "bool":
            nlu_bool = nlu.run(text=text, intent=intent)
            intent_name = nlu_bool['intent']['intentName']
            if intent_name == None:
                return False
            else:
                return intent_name

# Implémentation de l'état de mode rappel


class ReminderModeState(HubState):

    def handle_button_trigger(self, hub):
        print("Erreur : Impossible de passer en mode déclenchement de bouton en dehors de l'état de veille")

    def handle_standby(self, hub):
        hub.set_state(StandbyState())

    def handle_reminder(self, hub):
        print("Erreur : Impossible de rester dans l'état de mode rappel")

    def launch_tts(self, hub, file):
        # Lancement du TTS en mode lecture de fichier audio
        Speaker.sound(file)

    def send_message_via_websocket(self, hub, message):
        # Code pour envoyer un message via WebSocket
        server.send_to_all_clients(message)

    def speak_text(self, hub, text):
        # Lancement du TTS en mode lecture de texte
        Speaker.talk(text)

    def run_nlu(self, hub, text, intent):
        if intent == "choice":
            nlu_bool = nlu.run(text=text, intent=intent)
            intent_name = nlu_bool['intent']['intentName']
            if intent_name == None:
                return False
            else:
                return intent_name
        elif intent == "bool":
            nlu_bool = nlu.run(text=text, intent=intent)
            intent_name = nlu_bool['intent']['intentName']
            if intent_name == None:
                return False
            else:
                return intent_name


class WhisperState(HubState):
    def handle_rfid_trigger(self, hub):
        pass

    def handle_button_trigger(self, hub):
        pass

    def handle_reminder(self, hub):
        pass

    def handle_standby(self, hub):
        hub.set_state(StandbyState())

    def handle_self_state(self, hub):
        pass


# Classe principale du hub
class Hub:
    def __init__(self):
        self.message = None
        self.previous_message = None
        self.state = TestState()

    def set_state(self, state):
        print(
            f"Changement d'état : {self.state.__class__.__name__} -> {state.__class__.__name__}")
        self.state = state

    def get_state(self):
        return self.state

    def handle_message(self, message):
        self.state.handle_message(self, message)

    def get_received_message(self):
        return self.state.get_received_message()

    def handle_rfid_trigger(self):
        self.state.handle_rfid_trigger(self)

    def handle_button_trigger(self):
        self.state.handle_button_trigger(self)

    def handle_reminder(self):
        self.state.handle_reminder(self)

    def handle_standby(self):
        self.state.handle_standby(self)

    def handle_self_state(self):
        self.state.handle_self_state(self)

    def send_web_message(self, message):
        self.state.send_web_message(message)

    def websocket_connexion(self):
        return self.state.websocket_connexion(self)

    def communicate_with_ble(self):
        return self.state.communicate_with_ble(self)

    def launch_bluetooth(self):
        self.state.launch_bluetooth(self)

    def communicate_via_websocket(self, expected_message, messages):
        self.state.communicate_via_websocket(
            self, expected_message=expected_message)
        # Effectuer des opérations avec le WebSocket

    def send_message_via_websocket(self, message):
        self.state.send_message_via_websocket(self, message)

    def launch_tts(self, file):
        self.state.launch_tts(self, file)

    def speak_text(self, text):
        self.state.speak_text(self, text)

    def run_nlu(self, text, intent):
        return self.state.run_nlu(self, text, intent)

    def add_appointment(self, data, intent):
        return self.state.add_appointment(self, data, intent)

    def update_appointment_reminder(self, data, intent):
        return self.state.update_appointment_reminder(self, data, intent)


# Utilisation du hub
hub = Hub()
# server.handle_clients()
# # Exemple de scénarios
# while not hub.websocket_connexion():
#     pass

hub.send_web_message("Init")
nlu.fit()
hub.handle_standby()
# Durée en secondes pour les 8 minutes
duration = 8 * 60
# Temps de départ

start_time = time.time()  # Remplacez par votre temps de base
next_time = start_time
# time.sleep(10)
standbyInit = False
cardReader = True
counter = 0
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
while True:
    if isinstance(hub.get_state(), StandbyState):
        hub.send_web_message("Default")
        # hub.send_web_message("Default")
        rfid_trigger.read()  # This will run indefinitely
        card_state = rfid_trigger.get_state()

        is_intro_executed = False
        is_intro_choice_executed = False
        rfid_trigger.read()  # This will run indefinitely
        card_state = rfid_trigger.get_state()
        if not card_state:
            standbyInit = False
            cardReader = True
        if standbyInit:
            cardReader = False
        my_btn.checking_state()
        button_state = my_btn.pressed

        if button_state:
            hub.handle_button_trigger()

        if card_state and cardReader:
            hub.send_web_message("Connecting")
            hub.handle_rfid_trigger()

        current_time = datetime.now()  # Obtenir le temps actuel

        if time.time() > next_time:
            # Vérifier s'il y a un rappel à la temporalité actuelle
            current_appointment = manager.check_appointment(current_time)
            # current_appointment = manager.check_appointment(
            #     datetime.strptime("2023-06-30 17:30", "%Y-%m-%d %H:%M"))
            if current_appointment:
                hub.handle_reminder()
            else:
                for i in range(10):
                    target_time = current_time + timedelta(minutes=i)
                    appointment_exists = manager.check_appointment(target_time)
                    if appointment_exists:
                        hub.handle_reminder()
            base_time = time.time()

            # Attendre 1 minute avant la prochaine vérification
            next_time = base_time + 60
    elif isinstance(hub.get_state(), RecoveryState):

        if not is_intro_executed:
            firstpart = True
            secondpart = True
            thirdpart = True
            fourpart = True
            # hub.launch_bluetooth()
            # btn_value = hub.communicate_with_ble()
            hub.send_web_message("Connected")
            stepZero = True
            stepOne = False
            stepTwo = False
            stepThree = False
            stepFour = False
            btn_value = 1 - counter
            counter = counter + 1

        if btn_value is not None and btn_value > 0:
            if not is_intro_executed:

                hub.send_message_via_websocket("LED_static")
                hub.launch_tts(
                    "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/TTS/Digital-bell.wav")
                hub.speak_text("Bonjour ! Il semblerait que vous ayez pris " +
                               str(btn_value) + " rendez-vous aujourd’hui. Est-ce qu’on peut commencer ?")
                hub.send_message_via_websocket("Whisper_binary")

                is_intro_executed = True
            received_message = hub.get_received_message()
            if received_message:
                print("received_message ", received_message)
                print("step zero", stepZero)
                print("condition ", received_message.startswith("PC WhisperBool#"))
                if received_message.startswith("PC WhisperBool#") and stepZero:
                    print("###################    Bool#   #####################")
                    value = received_message.split("Bool#", 1)[1]
                    intent = "bool"
                    nlu_result = hub.run_nlu(text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter ?")
                        hub.send_message_via_websocket(
                            "Whisper_bool data_notOk")
                        received_message = None
                        nlu_result = None
                    else:
                        print("nlu_result", nlu_result)
                        if nlu_result == "negation":
                            hub.send_message_via_websocket("Whisper_bool no")
                            hub.speak_text(
                                "Très bien. Quand vous serez prêt, appuyer sur le bouton du hub et dites que vous souhaitez rentrer un rendez-vous.")
                            stepZero = False
                            btn_value = btn_value - 1
                            hub.handle_standby()
                            received_message = None

                        elif nlu_result == "affirmation":
                            hub.send_message_via_websocket("Whisper_bool yes")
                            hub.speak_text(
                                "Quelles sont les informations relatives à votre rendez-vous numéro 1 ?")
                            hub.send_message_via_websocket("Whisper")
                            stepZero = False
                            stepOne = True
                            received_message = None
                elif received_message.startswith("PC WhisperRdv#") and stepOne:
                    print("###################    Rdv#   #####################")
                    value = received_message.split("Rdv#", 1)[1]
                    intent = "rdv"
                    nlu_result = hub.run_nlu(
                        text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter ?")
                        hub.send_message_via_websocket(
                            "Whisper_rdv data_notOK")
                        received_message = None
                        nlu_result = None

                    else:
                        appointment = hub.add_appointment(nlu_result, intent)
                        formatted_date = datetime.strptime(
                            appointment['date'], "%Y-%m-%d").strftime("%A %d %B")
                        if not appointment['informations_supplementaires'] == "":
                            details = ". Les informations complémentaire sont " + \
                                appointment['informations_supplementaires']
                        else:
                            details = '.'
                        if appointment['titre'] == '':
                            appointment['titre'] = appointment['lieu']
                        hub.speak_text("Entendu. Je récapitule ! Vous avez " + appointment['titre'] + " le " + formatted_date +
                                       " à " + appointment['heure'] + details + ". Est-ce correct ?")
                        hub.send_message_via_websocket("Whisper_rdv data_OK")
                        stepOne = False
                        stepTwo = True
                        received_message = None
                elif received_message.startswith("PC WhisperBool#") and stepTwo:
                    print("###################    Bool#   #####################")
                    value = received_message.split("Bool#", 1)[1]
                    intent = "bool"
                    nlu_result = hub.run_nlu(text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter ?")
                        hub.send_message_via_websocket(
                            "Whisper_bool data_notOk")
                        received_message = None
                    elif nlu_result == "negation":
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous me répéter les information de votre rendez-vous ?")
                        hub.send_message_via_websocket("Whisper_bool no")
                        stepTwo = False
                        stepOne = True
                        received_message = None
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    elif nlu_result == "affirmation":
                        hub.send_message_via_websocket("Whisper_bool yes")
                        hub.speak_text(
                            "Entendu. A quelle heure souhaitez-vous être informé de ce rendez-vous ?")
                        hub.send_message_via_websocket("Whisper_remind start")
                        stepTwo = False
                        stepThree = True
                        received_message = None
                # # elif received_message.startswith("PC WhisperRdv#") and stepTwo:
                #     print("###################    Rdv#   #####################")
                #     value = received_message.split("Rdv#", 1)[1]
                #     received_message = None
                #     intent = "rdv"
                #     nlu_result = hub.run_nlu(
                #         text="je souhaite prendez un rendez-vous chez le médecin le 19 mai à 18h", intent=intent)
                #     if not nlu_result:
                #         hub.speak_text("Je n'ai pas bien compris votre réponse")
                #         hub.send_message_via_websocket("Whisper_rdv data_notOK")
                #         received_message = None

                #     elif firstpart:
                #         firstpart = False
                #         appointment = hub.add_appointment(nlu_result, intent)
                #         hub.speak_text("Vous avez un " + appointment['titre'] + " " + appointment['lieu'] +
                #                     " à " + appointment['heure'] + " le " + appointment['date'] + ". Est-ce correct ?")
                #         hub.send_message_via_websocket("Whisper_rdv data_OK")
                #         stepTwo = False
                #         stepThree = True
                # # elif received_message.startswith("PC WhisperBool#") and stepThree:
                #     print("###################    Bool#   #####################")
                #     value = received_message.split("Bool#", 1)[1]
                #     intent = "bool"
                #     nlu_result = hub.run_nlu(text="oui", intent=intent)
                #     if not nlu_result:
                #         hub.speak_text(
                #             "Je n'ai pas bien compris votre réponse, répétez votre rendez-vous s'il vous plaît.")
                #         hub.send_message_via_websocket("Whisper_bool data_notOK")
                #         received_message = None
                #     elif secondpart:
                #         secondpart = False
                #         hub.speak_text(
                #             "Très bien, à quelle heure souhaitez-vous avoir un rappel de votre rendez-vous ?")
                #         hub.send_message_via_websocket("Whisper_bool data_OK")
                #         received_message = None
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                elif received_message.startswith("PC WhisperRemind#") and stepThree:
                    print("###################    Remind#   #####################")
                    value = received_message.split("Remind#", 1)[1]
                    intent = "remind"
                    nlu_result = hub.run_nlu(
                        text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter l'heure de votre rappel ?")
                        hub.send_message_via_websocket(
                            "Whisper_remind data_notOK")
                        received_message = None
                    else:
                        appointment_reminder = hub.update_appointment_reminder(
                            nlu_result, intent)
                        hub.send_message_via_websocket(
                            "Whisper_remind data_OK")
                        hub.speak_text(
                            "Entendu. Vous souhaitez donc que je vous rappelle votre rendez-vous 30 minutes avant ?")
                        hub.send_message_via_websocket("Whisper_bool start")
                        received_message = None
                        stepThree = False
                        stepFour = True

                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                elif received_message.startswith("PC WhisperBool#") and stepFour:
                    print("###################    Bool#   #####################")

                    value = received_message.split("Bool#", 1)[1]
                    intent = "bool"
                    nlu_result = hub.run_nlu(text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous me dire si ces informations sont correcte ?")
                        hub.send_message_via_websocket(
                            "Whisper_bool data_notOk")
                        received_message = None
                    elif nlu_result == "negation":
                        hub.speak_text(
                            "Excusez moi je n’ai pas compris votre réponse, pouvez-vous me répéter à quelle heure vous souhaitez être informé de ce rendez-vous ?")
                        hub.send_message_via_websocket("Whisper_bool no")
                        stepFour = False
                        stepTree = True
                        received_message = None
                    elif nlu_result == "affirmation":
                        hub.send_message_via_websocket("Whisper_bool yes")
                        hub.speak_text(
                            "C’est noté. Je suis ravis d’avoir pu vous aider !")
                        stepFour = False
                        btn_value = btn_value-1
                        hub.handle_standby()
                        received_message = None

        else:
            standbyInit = True
            hub.handle_standby()
    elif isinstance(hub.get_state(), ButtonTriggerState):
        if not is_intro_choice_executed:
            hub.send_message_via_websocket("LED_static_2")
            hub.speak_text("Bonjour, comment puis-je vous aider ?")
            hub.send_message_via_websocket("Whisper_choice")
            step_choice_Zero = True
            step_choice_One = False
            is_intro_choice_executed = True
        received_message = hub.get_received_message()
        if received_message:
            if received_message.startswith("PC WhisperChoice#") and step_choice_Zero:
                print("###################    Choice#   #####################")
                value = received_message.split("Choice#", 1)[1]
                intent = "choice"
                nlu_result = hub.run_nlu(text=value, intent=intent)
                step_choice_Zero = False
                if not nlu_result:
                    hub.speak_text(
                        "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter ?")
                    hub.send_message_via_websocket("Whisper_choice data_notOk")
                    received_message = None
                    nlu_result = None
                if nlu_result == "summaryOfDay":
                    appointments = manager.get_daily_appointments()
                    resume_message = manager.transform_data_to_message(
                        appointments)
                    hub.speak_text(resume_message)
                    step_choice_Zero = False
                    step_choice_One = True
                    received_message = None
                    nlu_result = None
                    hub.send_message_via_websocket("Whisper_choice data_Ok")
                    hub.send_message_via_websocket("Whisper_bool start")
            elif received_message.startswith("PC WhisperBool#") and step_choice_One:
                print("###################    Bool#   #####################")
                value = received_message.split("Bool#", 1)[1]
                intent = "bool"
                nlu_result = hub.run_nlu(text=value, intent=intent)
                if not nlu_result:
                    hub.speak_text(
                        "Excusez moi je n’ai pas compris votre réponse, pouvez-vous répéter ?")
                    hub.send_message_via_websocket(
                        "Whisper_bool data_notOk")
                    received_message = None
                    nlu_result = None
                else:
                    print("nlu_result", nlu_result)
                    if nlu_result == "negation":
                        hub.send_message_via_websocket("Whisper_bool no")
                        hub.speak_text(
                            "Ravis d'avoir pu vous aider")
                        step_choice_One = False
                        hub.handle_standby()
                        received_message = None

                    elif nlu_result == "affirmation":
                        hub.send_message_via_websocket("Whisper_bool yes")
                        hub.speak_text(
                            "Excusez-moi, je n'ai pas compris votre demande")
                        hub.send_message_via_websocket("Whisper_choice")

            # appointments = manager.get_daily_appointments()
            # resume_message = manager.transform_data_to_message(appointments)
            # print(resume_message)
            # hub.speak_text(resume_message)

        my_btn.checking_state()
        button_state = my_btn.pressed

        # received_message = hub.get_received_message()
        # if received_message:
        #     if received_message.startswith("PC WhisperChoice#"):
        #         print("###################    Choice#   #####################")

        #         value = received_message.split("Choice#", 1)[1]
        #         intent = "choice"
        #         nlu_result = hub.run_nlu(
        #             text="avoir un récapitulatif de ma jounée", intent=intent)
        #         if not nlu_result:
        #             print(nlu_result)
        #             hub.speak_text(
        #                 "Excusez moi je n’ai pas compris votre réponse, pouvez-vous me dire si ces informations sont correcte ?")
        #             hub.send_message_via_websocket("Whisper_bool data_notOk")
        #             received_message = None
        #         elif nlu_result == "negation":
        #             hub.speak_text(
        #                 "Excusez moi je n’ai pas compris votre réponse, pouvez-vous me répéter à quelle heure vous souhaitez être informé de ce rendez-vous ?")
        #             hub.send_message_via_websocket("Whisper_bool no")
        #             stepFour = False
        #             stepTree = True
        #             received_message = None
        #         elif nlu_result == "affirmation":
        #             hub.send_message_via_websocket("Whisper_bool yes")
        #             hub.speak_text(
        #                 "C’est noté. Je suis ravis d’avoir pu vous aider !")
        #             stepFour = False
        #             btn_value = btn_value-1
        #             hub.handle_standby()
        #         received_message = None
        # si detection de récap

        if button_state:
            hub.handle_standby()
            hub.send_message_via_websocket("LED_off")
            time.sleep(1)
        # hub.send_web_message({"title": "Suppressed"})
        pass
    elif isinstance(hub.get_state(), ReminderModeState):
        appointment = manager.get_reminder_apointment()
        # hub.send_web_message()
        current_time = time.time()
        if not is_intro_executed:
            btn_was_pressed = False
            hub.send_message_via_websocket("LED_fade")
            is_intro_executed = True
            waiting_data = False
            print(appointment)
            difference_temps = datetime.strptime(
                appointment['heure'], "%H:%M") - datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
            hub.launch_tts(
                "/home/valentin/Desktop/MemoRoom/modules/_Liveo/TTS/Echo.wav")
        if current_time - start_time >= duration:
            hub.launch_tts(
                "/home/valentin/Desktop/MemoRoom/modules/_Liveo/TTS/Echo.wav")
            start_time = time.time()


# Convertir l'heure du rendez-vous en objet datetime
        # print("Bonjour ! Nous sommes le vendredi 16 juin il est 10:00. Vous avez un rendez-vous à 10:30, soit dans 30 minutes, chez votre médecin traitant, veillez à ne pas oublier votre carte vitale. Souhaitez vous que je répète ?")
        # print("Bonjour ! Nous sommes le", datetime.now().strftime("%A %d %B"), "il est", datetime.now().strftime("%H:%M"), ". Vous avez un rendez-vous à ",datetime.strptime(appointment['heure'], "%H:%M"), ", soit dans ",difference_temps," pour ",appointment["titre"],".")

        my_btn.checking_state()
        button_state = my_btn.pressed
        if button_state:
            btn_was_pressed = True
        if btn_was_pressed:
            if not waiting_data:
                hub.send_message_via_websocket("LED_off")
                if appointment["titre"] == "":
                    appointment["titre"] = appointment["lieu"]
                if str(difference_temps).split(":")[0] == '' or str(difference_temps).split(":")[0] == '00' or str(difference_temps).split(":")[0] == '0':
                    difference_heure = ""
                else:
                    difference_heure = str(difference_temps).split(":")[
                        0] + " heure et "
                if str(difference_temps).split(":")[1] == '':
                    difference_minutes = ""
                else:
                    difference_minutes = "29" + " minutes"

                # message = "Bonjour ! Nous sommes le " + datetime.now().strftime("%A %d %B") + " il est " + datetime.now().strftime("%H:%M") + ". Vous avez un rendez-vous à " + \
                #     appointment['heure'] + ", soit dans " + str(difference_temps).split(":")[0] + " heure et " + str(
                #         difference_temps).split(":")[1] + " minutes pour " + appointment["titre"] + "."
                # web = {
                #     'titre': "remind",
                #     'data': {'titre': appointment['titre'], 'heure': appointment['heure']}
                # }
                message = "Bonjour ! Nous sommes le vendredi 30 juin il est 18h01. Vous avez un rendez-vous à " + \
                    appointment['heure'] + ", soit dans " +\
                    difference_minutes + " pour " + \
                    appointment["titre"] + "."
                web = {
                    'titre': "remind",
                    'data': {'titre': appointment['titre'], 'heure': appointment['heure']}
                }
                hub.send_web_message(web)
                hub.speak_text(message)
                hub.speak_text("Souhaitez vous que je répète ?")
                hub.send_message_via_websocket("Whisper_bool start")
            received_message = hub.get_received_message()
            waiting_data = True
            if received_message:
                if received_message.startswith("PC WhisperBool#"):
                    print("###################    Bool#   #####################")
                    value = received_message.split("Bool#", 1)[1]
                    intent = "bool"
                    nlu_result = hub.run_nlu(text=value, intent=intent)
                    if not nlu_result:
                        hub.speak_text(
                            "Je n'ai pas bien compris votre réponse, pouvez-vous répéter s'il vous plaît.")
                        hub.send_message_via_websocket(
                            "Whisper_remind data_notOk")
                        received_message = None
                    else:
                        hub.speak_text(
                            "Ravis d'avoir pu vous aider !")
                        hub.send_message_via_websocket(
                            "Whisper_remind data_Ok")
                        hub.handle_standby()
                        # hub.speak_text(
                        #     "Autant pour moi, je vous répète")
                        # hub.send_message_via_websocket(
                        #     "Whisper_remind data_Ok")
                        waiting_data = False
                        received_message = None
            pass  # Sortir de la boucle dès qu'un rendez-vous est trouvé
