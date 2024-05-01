from WSServer import WSServer

# Adresse IP et port du serveur
server_address = '192.168.1.16'
server_port = 8765

# Création de l'instance du serveur
server = WSServer(server_address, server_port)

# Démarrage du serveur WebSocket
server.start()
print("Serveur WebSocket démarré.")

# Boucle principale pour gérer les clients
while True:
    # Gestion des clients et des messages entrants
    server.handle_clients()

    # Conditions de sortie de la boucle
    if False:
        break

# Arrêt du serveur WebSocket
server.stop()
