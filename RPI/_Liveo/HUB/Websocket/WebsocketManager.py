import socket
import select
import time
from datetime import datetime


class WSServerState:
    def handle_clients(self, server):
        pass

    def handle_message(self, server, message, client_socket, tts, nlu, appointment):
        pass


class WSServerStateRunning(WSServerState):
    def handle_message(self, server, message, client_socket, tts=None, nlu=None, appointment=None):
        if message == "START":
            server.send_to_all_clients("Server is running")
        elif message == "STOP":
            server.send_to_all_clients("Server is stopped")
        elif message == "PING":
            server.send_to_all_clients("LED_PONG")
        elif message == "DISCONNECT":
            server.send_to_all_clients(
                "Client disconnected: " + str(client_socket.getpeername()))
            server.clients.remove(client_socket)
            client_socket.close()
        elif message == "LED_STATE":
            server.send_to_all_clients(self.get_current_state())
        elif message == "Fade_mode":
            server.set_led_status("Fade_mode")
        elif message == "Static_mode":
            server.set_led_status("Static_mode")
        elif message == "Off_mode":
            server.set_led_status("Off_mode")
            pass

        # elif message.split("Rdv#", 1)[0] == "PC Whisper":
        #     # Récupère l'analyse Whisper
        #     value = message.split("Rdv#", 1)[1]
        #     # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     # nlu_rdv = nlu.run(text=value, intent="rdv")
        #     # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     print("FAKED RESULT")
        #     nlu_rdv = nlu.run(
        #         text="je souhaite prendez un rendez-vous chez le médecin le 19 mai à 18h", intent="rdv")

        #     print(nlu_rdv)
        #     intent_name = nlu_rdv['intent']['intentName']
        #     print(intent_name)
        #     if intent_name == None:
        #         tts.talk(
        #             "Je n'ai pas bien compris votre réponse")
        #         server.send_to_all_clients(
        #             "Whisper_rdv data_notOK")
        #         delay_start_time = time.time()
        #     else:
        #         json_data = {
        #             "id": 0,
        #             "date": "",
        #             "heure": "",
        #             "lieu": "",
        #             "titre": "",
        #             "informations_supplementaires": "",
        #             "rappel": {
        #                 "date": "",
        #                 "heure": ""
        #             }
        #         }
        #         for slot in nlu_rdv['slots']:
        #             if slot['slotName'] == 'date':
        #                 date_value = slot['value']['value']
        #                 date_parsed = datetime.strptime(
        #                     date_value, "%Y-%m-%d %H:%M:%S %z")
        #                 json_data['date'] = date_parsed.strftime(
        #                     "%Y-%m-%d")
        #             elif slot['slotName'] == 'heure':
        #                 heure_value = slot['value']['value']
        #                 heure_parsed = datetime.strptime(
        #                     heure_value, "%Y-%m-%d %H:%M:%S %z")
        #                 json_data['heure'] = heure_parsed.strftime(
        #                     "%H:%M")
        #             elif slot['slotName'] == 'lieu':
        #                 json_data['lieu'] = slot['value']['value']
        #             elif slot['slotName'] == 'type_rendez_vous':
        #                 json_data['titre'] = slot['value']['value']
        #             elif slot['slotName'] == 'informations_supplementaires':
        #                 json_data['informations_supplementaires'] = slot['value']['value']
        #         json_data['id'] = -1
        #         print(json_data)
        #         appointment.add_appointment(json_data)
        #         tts.talk("Vous avez un "+json_data['titre']+json_data['lieu']+" à " +
        #                  json_data['heure']+" le "+json_data['date']+". Est-ce correct ?")
        #         # server.send_to_all_clients("Whisper Bool")
        #         server.send_to_all_clients(
        #             "Whisper_rdv data_OK")

        # elif message == "Whisper_rdv nextCommand":
        #     server.send_to_all_clients("Whisper Bool")
        # elif message.split("Bool#", 1)[0] == "PC Whisper":
        #     # Récupère l'analyse Whisper
        #     value = message.split("Bool#", 1)[1]
        #     # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     # nlu_bool = nlu.run(text=value, intent="bool")
        #     # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     print("FAKED RESULT")
        #     nlu_bool = nlu.run(
        #         text="Oui", intent="bool")

        #     print(nlu_bool)
        #     intent_name = nlu_bool['intent']['intentName']
        #     print(intent_name)
        #     if intent_name == None or intent_name == "negation":
        #         tts.talk(
        #             "Je n'ai pas bien compris votre réponse, répétez votre rendez-vous s'il vous plait.")
        #         server.send_to_all_clients(
        #             "Whisper_bool data_notOK")
        #         delay_start_time = time.time()
        #     else:
        #         time.sleep(1/10)
        #         server.send_to_all_clients(
        #             "Whisper_bool data_OK")
        # elif message == "Whisper_bool nextCommand":
        #     tts.talk(
        #         "Très bien, à quelle heure souhaitez-vous avoir un rappel de votre rendez-vous ?")
        #     server.send_to_all_clients("Whisper Remind")
        # elif message.split("Remind#", 1)[0] == "PC Whisper":
        #     # Récupère l'analyse Whisper
        #     value = message.split("Remind#", 1)[1]
        #     # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     # nlu_remind = nlu.run(text=value, indent="remind")
        #     # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
        #     print("FAKED RESULT")
        #     nlu_remind = nlu.run(
        #         text="Je veux mettre un rappel pour ma consultation le 5 septembre à 9h", intent="remind")
        #     print(nlu_remind)
        #     intent_name = nlu_remind['intent']['intentName']
        #     print(intent_name)
        #     if intent_name == None:
        #         tts.talk(
        #             "Je n'ai pas compris votre réponse, pouvez-vous répéter l'heure de votre rendez-vous ?")
        #         server.send_to_all_clients(
        #             "Whisper_remind data_notOK")
        #         delay_start_time = time.time()
        #     else:

        #         json_data_remind = {
        #             "id": 0,
        #             "date": "",
        #             "heure": "",
        #             "lieu": "",
        #             "titre": "",
        #             "informations_supplementaires": "",
        #             "rappel": {
        #                 "date": "",
        #                 "heure": ""
        #             }
        #         }

        #         for slot in nlu_remind['slots']:
        #             if slot['slotName'] == 'date':
        #                 date_value = slot['value']['value']
        #                 date_parsed = datetime.strptime(
        #                     date_value, "%Y-%m-%d %H:%M:%S %z")
        #                 json_data_remind["rappel"]["date"] = date_parsed.strftime(
        #                     "%Y-%m-%d")
        #             elif slot['slotName'] == 'time':
        #                 heure_value = slot['value']['value']
        #                 heure_parsed = datetime.strptime(
        #                     heure_value, "%Y-%m-%d %H:%M:%S %z")
        #                 json_data_remind["rappel"]["heure"] = heure_parsed.strftime(
        #                     "%H:%M")
        #         json_data_remind['id'] = -1
        #         print(json_data_remind)
        #         appointment.update_appointment_reminder(
        #             json_data_remind['id'], json_data_remind["rappel"])
        #         server.send_to_all_clients(
        #             "Whisper_remind data_OK")
        #         tts.talk(
        #             "c'est noté, ravis d'avoir pu vous aider")
        #         appointment.reset_appointment_ids()
        #         server.whisperState(
        #             "Ended")
        return message

    def handle_clients(self, server):
        inputs = [server.server_socket] + server.clients
        outputs = []

        try:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)

            for sock in readable:
                if sock is server.server_socket:
                    # Nouvelle connexion entrante
                    client_socket, client_address = server.server_socket.accept()
                    print("Nouvelle connexion client :", client_address)
                    client_socket.setblocking(0)
                    server.clients.append(client_socket)
                else:
                    # Données reçues d'un client existant
                    try:
                        message = sock.recv(1024)
                        if message:
                            # Traitez le message reçu ici
                            message = message.decode("utf-8")
                            if not message == "PING":
                                print("Message reçu :", message)
                            server.received_messages.append(message)
                        else:
                            # Connexion fermée par le client
                            print("Connexion fermée :", sock.getpeername())
                            sock.close()
                            server.clients.remove(sock)
                    except:
                        pass
        except:
            pass


class WSServer:
    def __init__(self, address, port):
        self.server_address = address
        self.server_port = port
        self.server_socket = None
        self.clients = []
        self.received_messages = []
        self.state = WSServerStateRunning()
        self.led_status = "Off_mode"
        self.newStateWhisper = "NotStarted"
        self.pc = False
        self.LED = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Serveur WebSocket démarré.")

    def checkID(self):
        if self.pc and self.LED:
            return True
        else:
            return False

    def handle_clients(self):
        self.state.handle_clients(self)

    def send_to_all_clients(self, message):
        if message == "Fade_mode":
            self.set_led_status("Fade_mode")
        elif message == "Static_mode":
            self.set_led_status("Static_mode")
        elif message == "Off_mode":
            self.set_led_status("Off_mode")

        else:
            if not message == "LED_PONG":
                pass
        for client_socket in self.clients:
            try:
                if not message == "LED_PONG":
                    print("Message envoyé :", message)
                client_socket.sendall(message.encode("utf-8"))
            except ConnectionResetError:
                client_socket.close()
                self.clients.remove(client_socket)
                print("Connexion réinitialisée :", client_socket.getpeername())

    def get_received_messages(self):
        messages = self.received_messages.copy()
        self.received_messages.clear()
        return messages

    def get_led_status(self):
        return self.led_status

    def whisperState(self, state=None):
        if state:
            self.newStateWhisper = state
        return self.newStateWhisper

    def stop(self):
        for client_socket in self.clients:
            client_socket.close()
        self.clients = []

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            print("Serveur WebSocket arrêté.")


class WSClient:
    def __init__(self, server_address, server_port, client_id):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.client_id = client_id

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connected to the WebSocket server.")

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.sendall(message.encode("utf-8"))

    def receive_message(self):
        if self.client_socket:
            message = self.client_socket.recv(1024)
            if message:
                return message.decode("utf-8")

        return None

    def get_id(self):
        return self.client_id

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print("Disconnected from the WebSocket server.")
