from Tornato_WebSocket_Raspberry.client import TornadoWebsocketClient

myClient = TornadoWebsocketClient()
myClient.connect()
myClient.send("Hello")
while True:
    myClient.run()