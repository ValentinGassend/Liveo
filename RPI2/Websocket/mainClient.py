from WebsocketManager import WSClient
client = WSClient("192.168.1.18", 8082, "LED")
client.connect()

try:
       while True:
           
            received_message = client.receive_message()
            if received_message:
                 print("Message reçu du serveur : "+received_message)
            if received_message == "ID":
                print("Message sent to the server: '" + client.get_id() + "'")
                client.send_message(client.get_id())
            elif received_message == "LED_off":
                pass
except KeyboardInterrupt:
    # Close the client connection when Ctrl+C is pressed
    client.close()
