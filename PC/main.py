from datetime import datetime
from WebSocket.WSClient import WSClient
from PyWhisperCpp.Myassistant import MyAssistant
import keyboard

neverStarted = True
# Adresse IP et port du serveur
server_address = '192.168.1.16'


# server_address = '192.168.43.242'
server_port = 8081

# Création de l'instance du client
client = WSClient(server_address, server_port)
Id = "PC"


def MyCallbackRDV(data):
    print(data)
    client.send_message(Id + " WhisperRdv#" + data)
    my_assistant_RDV.close()


def MyCallbackBool(data):
    print(data)
    client.send_message(Id + " WhisperBool#" + data)
    my_assistant_bool.close()


def MyCallbackRemind(data):
    print(data)
    client.send_message(Id + " WhisperRemind#" + data)
    my_assistant_remind.close()
    
def MyCallbackChoice(data):
    print(data)
    client.send_message(Id + " WhisperChoice#" + data)
    my_assistant_choice.close()


my_assistant = False
previousResponse = False
id_not_recieved = True
while True:

    if neverStarted:
        neverStarted = False
        client.connect()
        my_assistant_RDV = MyAssistant(model='medium', commands_callback=MyCallbackRDV,
                                      n_threads=10, input_device=0, q_threshold=6, silence_threshold=50)
        my_assistant_remind = MyAssistant(model='medium', commands_callback=MyCallbackRemind,
                                          n_threads=10, input_device=0, q_threshold=6, silence_threshold=50)
        my_assistant_bool = MyAssistant(model='small', commands_callback=MyCallbackBool,
                                                n_threads=10, input_device=0, q_threshold=6, silence_threshold=50)
        my_assistant_choice = MyAssistant(model='medium', commands_callback=MyCallbackChoice,
                                                n_threads=10, input_device=0, q_threshold=6, silence_threshold=50)

    # Réception de la réponse du serveur
    response = str(client.receive_message())

    if not previousResponse == response:
        if not response == "LED_PONG":
            print("Réponse du serveur : '" + response + "'")
    previousResponse = response

    if response == "ID" and id_not_recieved:
        print("Message envoyé au serveur : '" + Id + "'")
        client.send_message(Id)
    if response == "PC_ok":
        id_not_recieved=False
    if response == "Whisper":
        my_assistant_bool.close()
        my_assistant_remind.close()
        my_assistant_RDV.start()
        response=None
    if response == "Whisper_reminder":
        my_assistant_bool.start()
        response=None
    if response == "Whisper_binary":
        my_assistant_bool.start()
        response=None
    if response == "Whisper_choice":
        response=None
        my_assistant_choice.start()
    if response == "Whisper_choice":
        response=None
        my_assistant_choice.start()
    if response == "Whisper_choice data_Ok":
        my_assistant_choice.close()
        response=None
    if response == "Whisper_remind data_OK":
        my_assistant_bool.close()
        response=None
    if response == "Whisper_bool data_notOk":
        my_assistant_bool.close()
        response=None
    if response == "Whisper_bool no":
        my_assistant_bool.close()
        response=None
    if response == "Whisper_bool yes":
            
        my_assistant_bool.close()
        response=None
    if response == "Whisper_remind data_notOK":
                
        my_assistant_bool.close()
        my_assistant_bool.start()
        response=None

    if response == "Whisper_rdv data_notOK":
        my_assistant_RDV.close()
        my_assistant_RDV.start()
        response=None

    if response == "Whisper_rdv data_OK":
        my_assistant_RDV.close() 
        my_assistant_bool.start()
        response=None

    if response == "Whisper_bool data_notOK":
        my_assistant_bool.close()
        my_assistant_bool.start()
        response=None
    if response == "Whisper_bool start":
        my_assistant_bool.start()
        response=None

    if response == "Whisper_bool data_OK":
        my_assistant_bool.close()
        response=None

    if response == "Whisper_remind start":
        my_assistant_remind.start()
        response=None

    if response == "Whisper_remind data_notOK":
        my_assistant_remind.close()
        response=None

    if response == "Whisper_remind data_OK" :
        my_assistant_remind.close()
        response=None

    try:
        if keyboard.is_pressed('q'):
            client.close()
            if my_assistant:
                my_assistant.close()
            neverStarted = True
            break
    except:
        pass