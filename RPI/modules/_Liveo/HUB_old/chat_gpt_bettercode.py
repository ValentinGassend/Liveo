from WebSocket.WSServer import WSServer
from NLU.nlu import Nlu
from TTS.tts import TTS
from Database_Reminder.meeting import Meeting
import signal
import sys
import time
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


class WebSocketServer:
    def __init__(self, address, port):
        self.server = WSServer(address, port)
        self.received_messages = []
        signal.signal(signal.SIGINT, self.signal_handler)

    def start(self):
        self.server.start()

    def handle_clients(self):
        self.server.handle_clients()

    def get_received_messages(self):
        self.received_messages = self.server.get_received_messages()
        return self.received_messages

    def send_to_all_clients(self, message):
        self.server.send_to_all_clients(message)

    def signal_handler(self, signal, frame):
        print('Arrêt du serveur WebSocket.')
        sys.exit(0)


class MeetingManager:
    def __init__(self, data_path):
        self.meeting_manager = Meeting(data_path)

    def check_current_date(self):
        self.meeting_manager.check_current_date()

    def update(self, data):
        self.meeting_manager.update(data)


class NLUTranslator:
    def __init__(self):
        self.translator = Nlu()
        self.fited = False

    def fit_rdv(self):
        self.translator.fit_rdv()

    def fit_choice(self):
        self.translator.fit_choice()

    def fit_bool(self):
        self.translator.fit_bool()

    def fit_remind(self):
        self.translator.fit_remind()
        self.fited = True

    def run_rdv(self, text):
        # ATTENTION : Le traitement est désactivé pour le moment
        # return self.translator.run(text)
        # FAUX RÉSULTAT POUR LES TESTS
        return {
            'intent': {'intentName': 'prendezerdv'},
            'slots': [
                {'slotName': 'date', 'value': {'value': '2023-05-31 18:00:00 +0000'}},
                {'slotName': 'lieu', 'value': {'value': 'médecin'}},
                {'slotName': 'type_rendez_vous', 'value': {'value': 'consultation'}}
            ]
        }

    def run_bool(self, text):
        # ATTENTION : Le traitement est désactivé pour le moment
        # return self.translator.run(text)
        # FAUX RÉSULTAT POUR LES TESTS
        return {
            'intent': {'intentName': 'affirmation'}
        }

    def run_remind(self, text):
        # ATTENTION : Le traitement est désactivé pour le moment
        # return self.translator.run(text)
        # FAUX RÉSULTAT POUR LES TESTS
        return {
            'intent': {'intentName': 'rappel'},
            'slots': [
                {'slotName': 'reminder_datetime', 'value': {
                    'value': '2023-09-05 09:00:00 +0000'}}
            ]
        }


class TextToSpeech:
    def __init__(self):
        self.speaker = TTS()

    def talk(self, text):
        self.speaker.talk(text)


if __name__ == "__main__":
    server_address = '192.168.43.242'
    server_port = 8082

    server = WebSocketServer(server_address, server_port)
    server.start()

    meeting_manager = MeetingManager(
        "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/Database_Reminder/data.json")

    nlu_translator = NLUTranslator()
    nlu_translator.fit_rdv()
    nlu_translator.fit_choice()
    nlu_translator.fit_bool()
    nlu_translator.fit_remind()

    tts = TextToSpeech()

    computer = False
    delay_start_time = None
    AgendaPressedNumber = False
    ID_PC = False

    while True and nlu_translator.fited:
        server.handle_clients()
        meeting_manager.check_current_date()
        received_messages = server.get_received_messages()

        if received_messages:
            for message in received_messages:
                print(message)

                if message == "PC":
                    server.send_to_all_clients("Whisper")

                if message.split("Rdv#", 1)[0] == "PC Whisper":
                    value = message.split("Rdv#", 1)[1]
                    print("FAKED RESULT")
                    nlu_rdv = nlu_translator.run_rdv(
                        text="je souhaite prendez un rendez-vous chez le médecin le 19 mai à 18h")

                    print(nlu_rdv)
                    intent_name = nlu_rdv['intent']['intentName']
                    print(intent_name)

                    if intent_name is None:
                        tts.talk("Je n'ai pas bien compris votre réponse")
                        server.send_to_all_clients("Whisper_rdv data_notOK")
                        delay_start_time = time.time()
                    else:
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

                        for slot in nlu_rdv['slots']:
                            if slot['slotName'] == 'date':
                                date_value = slot['value']['value']
                                date_parsed = datetime.strptime(
                                    date_value, "%Y-%m-%d %H:%M:%S %z")
                                json_data['date'] = date_parsed.strftime(
                                    "%A %d %B")
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
                        tts.talk("Vous avez un " + json_data['titre'] + json_data['lieu'] + " à " +
                                 json_data['heure'] + " le " + json_data['date'] + ". Est-ce correct ?")
                        server.send_to_all_clients("Whisper_rdv data_OK")

                elif message == "Whisper_rdv nextCommand":
                    server.send_to_all_clients("Whisper Bool")

                elif message.split("Bool#", 1)[0] == "PC Whisper":
                    value = message.split("Bool#", 1)[1]
                    print("FAKED RESULT")
                    nlu_bool = nlu_translator.run_bool(text="Oui")

                    print(nlu_bool)
                    intent_name = nlu_bool['intent']['intentName']
                    print(intent_name)

                    if intent_name is None or intent_name == "negation":
                        tts.talk(
                            "Je n'ai pas bien compris votre réponse, répétez votre rendez-vous s'il vous plait.")
                        server.send_to_all_clients("Whisper_bool data_notOK")
