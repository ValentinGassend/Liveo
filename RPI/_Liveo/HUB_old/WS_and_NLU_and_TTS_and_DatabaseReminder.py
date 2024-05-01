import webbrowser
from WebSocket.WSServer import WSServer
from NLU.nlu import Nlu
from TTS.tts import TTS
from Database_Reminder.meeting import Meeting
from rfid_and_BLE.rfid_BLE_manager import Rfid_BLE_manager
import signal
import sys
import time
import json
from datetime import datetime
import subprocess
import locale
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")

url = "http://192.168.43.242:8082/"

subprocess.run("sudo modprobe snd_bcm2835", shell=True)


def signal_handler(signal, frame):
    print('Arrêt du serveur WebSocket.')
    sys.exit(0)


MyManager = Rfid_BLE_manager(numDevice=2)
#################### Meeting Manager ######################
MyMeetingManager = Meeting(
    "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/Database_Reminder/data.json")

############# Natural Laguage Understanding ###############
fited = False
MyTraductor = Nlu()
# MyTraductor.fit_rdv()
# MyTraductor.fit_choice()
# MyTraductor.fit_bool()
# MyTraductor.fit_remind()
print("fited")
fited = True
########################### TTS ###########################

MySpeaker = TTS()


#############            WebSocket            #############
server_address = '192.168.1.16'
server_port = 8082
server = WSServer(server_address, server_port)
server.start()
computer = False
signal.signal(signal.SIGINT, signal_handler)
delay_start_time = None
AgendaPressedNumber = False
ID_PC = False
LED_rappel = False
last_sound_time = None
while True and fited:
    server.handle_clients()
    if MyManager.lunch():
        MySpeaker.sound(
            "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/TTS/Digital-bell.wav")
        server.send_to_all_clients(
            "LED_static")
    else:
        if MyMeetingManager.check_current_date():
            if not LED_rappel:
                server.send_to_all_clients(
                    "LED_rappel")
                LED_rappel = True
            if last_sound_time is None or time.time() - last_sound_time >= 300:
                MySpeaker.sound(
                    "/home/valentin/Desktop/MemoRoom/modules/_Liveo/HUB/TTS/Echo.wav")
                last_sound_time = time.time()
        received_messages = server.get_received_messages()
        # server.handle_clients()
        if received_messages:
            for message in received_messages:
                print(message)
                if message == "PC":
                    server.send_to_all_clients("Whisper")
                if message.split("Rdv#", 1)[0] == "PC Whisper":
                    # Récupère l'analyse Whisper
                    value = message.split("Rdv#", 1)[1]
                    # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    nlu_rdv = MyTraductor.run_rdv(text=value)
                    # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    # print("FAKED RESULT")
                    # nlu_rdv = MyTraductor.run_rdv(
                    #     text="je souhaite prendez un rendez-vous chez le médecin le 19 mai à 18h")

                    print(nlu_rdv)
                    intent_name = nlu_rdv['intent']['intentName']
                    print(intent_name)
                    if intent_name == None:
                        MySpeaker.talk(
                            "Je n'ai pas bien compris votre réponse")
                        server.send_to_all_clients(
                            "Whisper_rdv data_notOK")
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
                        MySpeaker.talk("Vous avez un "+json_data['titre']+json_data['lieu']+" à " +
                                       json_data['heure']+" le "+json_data['date']+". Est-ce correct ?")
                        # server.send_to_all_clients("Whisper Bool")
                        server.send_to_all_clients(
                            "Whisper_rdv data_OK")

                elif message == "Whisper_rdv nextCommand":
                    server.send_to_all_clients("Whisper Bool")
                elif message.split("Bool#", 1)[0] == "PC Whisper":
                    # Récupère l'analyse Whisper
                    value = message.split("Bool#", 1)[1]
                    # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    nlu_bool = MyTraductor.run_bool(text=value)
                    # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    # print("FAKED RESULT")
                    # nlu_bool = MyTraductor.run_bool(
                    #     text="Oui")

                    print(nlu_bool)
                    intent_name = nlu_bool['intent']['intentName']
                    print(intent_name)
                    if intent_name == None or intent_name == "negation":
                        MySpeaker.talk(
                            "Je n'ai pas bien compris votre réponse, répétez votre rendez-vous s'il vous plait.")
                        server.send_to_all_clients(
                            "Whisper_bool data_notOK")
                        delay_start_time = time.time()
                    else:

                        server.send_to_all_clients(
                            "Whisper_bool data_OK")
                elif message == "Whisper_bool nextCommand":
                    MySpeaker.talk(
                        "Très bien, à quelle heure souhaitez-vous avoir un rappel de votre rendez-vous ?")
                    server.send_to_all_clients("Whisper Remind")
                elif message.split("Remind#", 1)[0] == "PC Whisper":
                    # Récupère l'analyse Whisper
                    value = message.split("Remind#", 1)[1]
                    # ATTENTION DESACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    nlu_remind = MyTraductor.run_remind(text=value)
                    # ATTENTION ACTIVER CAR TRAITEMENT IMPOSSIBLE POUR LE MOMENT
                    # print("FAKED RESULT")
                    # nlu_remind = MyTraductor.run_remind(
                    #     text="Je veux mettre un rappel pour ma consultation le 5 septembre à 9h")
                    print(nlu_remind)
                    intent_name = nlu_remind['intent']['intentName']
                    print(intent_name)
                    if intent_name == None:
                        MySpeaker.talk(
                            "Je n'ai pas compris votre réponse, pouvez-vous répéter l'heure de votre rendez-vous ?")
                        server.send_to_all_clients(
                            "Whisper_remind data_notOK")
                        delay_start_time = time.time()
                    else:

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

                        for slot in nlu_remind['slots']:
                            if slot['slotName'] == 'reminder_datetime':
                                date_value = slot['value']['value']
                                date_parsed = datetime.strptime(
                                    date_value, "%Y-%m-%d %H:%M:%S %z")
                                json_data_remind["rappel"]["date"] = date_parsed.strftime(
                                    "%A %d %B")
                            elif slot['slotName'] == 'reminder_datetime':
                                heure_value = slot['value']['value']
                                heure_parsed = datetime.strptime(
                                    heure_value, "%Y-%m-%d %H:%M:%S %z")
                                json_data_remind["rappel"]["heure"] = heure_parsed.strftime(
                                    "%H:%M")
                        json_data_remind['id'] = -1
                        print(json_data)
                        MyMeetingManager.update(
                            {"rappel": json_data_remind["rappel"]})
                        server.send_to_all_clients(
                            "Whisper_remind data_OK")
                        MySpeaker.talk(
                            "c'est noté, ravis d'avoir pu vous aider")

                elif message == "LED":
                    server.send_to_all_clients("LED_off")
