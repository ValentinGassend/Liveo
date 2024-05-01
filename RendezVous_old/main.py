from WebSocket.MyWSClient import WSClient
from PyWhisperCpp.Myassistant import MyAssistant
import keyboard
neverStarted = True
# Adresse IP et port du serveur
server_address = '192.168.1.16'
server_port = 8082

# Création de l'instance du client
client = WSClient(server_address, server_port)
Id = "PC"


def MyCallbackRDV(data):
    print(data)
    client.send_message(Id + " WhisperRdv#"+data)
    my_assistant_RDV.close()

def MyCallbackBool(data):
    print(data)
    client.send_message(Id + " WhisperBool#"+data)
    my_assistant_bool.close()

def MyCallbackRemind(data):
    print(data)
    client.send_message(Id + " WhisperRemind#"+data)
    my_assistant_remind.close()

my_assistant = False
previousResponse = False
while True:
    
    if neverStarted:
        neverStarted = False
        client.connect()
        
        # client.send_message('Connected')
    # Réception de la réponse du serveur
    response = str(client.receive_message())
    
    if not previousResponse == response:
        print("Réponse du serveur : '"+response+"'")
    previousResponse = response
    if response == "ID":
        print("Message envoyé au serveur : '" + Id+"'")
        client.send_message(Id)
    if response == "Whisper":
        my_assistant_RDV = MyAssistant(model='medium', commands_callback=MyCallbackRDV,
                                n_threads=10, input_device=0, q_threshold=6)
        
        my_assistant_bool = MyAssistant(model='small', commands_callback=MyCallbackBool,
                                n_threads=10, input_device=0, q_threshold=6)
        
        my_assistant_remind = MyAssistant(model='medium', commands_callback=MyCallbackRemind,
                                n_threads=10, input_device=0, q_threshold=6)
        my_assistant_RDV.start()
    if response =="Whisper_rdv data_notOK":
        my_assistant_RDV.close()
        my_assistant_RDV.start()
    if response =="Whisper_rdv data_OK":
        my_assistant_RDV.close()
        client.send_message("Whisper_rdv nextCommand")
    if response =="Whisper Bool":
        my_assistant_bool.start()
    if response =="Whisper_bool data_notOK":
        my_assistant_bool.close()
        my_assistant_bool.start()
    if response =="Whisper_bool data_OK":
        my_assistant_bool.close()
        client.send_message("Whisper_bool nextCommand")
    if response =="Whisper Remind":
        my_assistant_remind.start()
    if response =="Whisper_remind data_notOK":
        my_assistant_remind.close()
        my_assistant_remind.start()
    if response =="Whisper_remind data_OK":
        my_assistant_remind.close()
    if KeyboardInterrupt==True:
        client.close()
        if my_assistant:
            my_assistant.close()
        neverStarted = True
    
        break
    # else:
    #     print("Wasn't the requested response from Server")
    #     print("serveur will shutdown")
    #     client.close()       
    # client.close()


