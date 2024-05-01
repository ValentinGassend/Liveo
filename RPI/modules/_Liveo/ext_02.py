from TTS.tts import TTS
import time
myTTS = TTS()
# from Tornato_WebSocket_Raspberry.server import TornadoWebsocketServer
from Tornato_WebSocket_Raspberry.client import TornadoWebsocketClient

# file = open('./cache.txt', 'r+')
with open('./cache.txt', 'r') as f:
    line = f.readline()


# myServer = TornadoWebsocketServer()
myClient = TornadoWebsocketClient()
myClient.connect()

# value = int(line)
# print(value)
# myTTS.talk("Bonjour ! Il semblerait que vous ayez pris "+str(value)+" rendez-vous aujourd’hui. Est-ce qu’on peut commencer ?")
# time.sleep(5)



# for i in range(value):
#   print(i)