from WSClient import WSClient

# Adresse IP et port du serveur
server_address = '192.168.1.16'
server_port = 8765

# Création de l'instance du client
client = WSClient(server_address, server_port)

# Connexion au serveur WebSocket
client.connect()
print("Connecté au serveur WebSocket.")

# Boucle principale pour traiter les messages entrants
while True:
    # Envoi d'un message au serveur
    message = input("Message à envoyer au serveur : ")
    client.send_message(message)

    # Réception de la réponse du serveur
    response = client.receive_message()
    print("Réponse du serveur :", response)

    # Conditions de sortie de la boucle
    if response == "Leave" or response is None:
        break

# Fermeture de la connexion
client.close()
