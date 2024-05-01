from WSServer import WSServer

# Création de l'instance du serveur WebSocket
server = WSServer("localhost", 8000)

# Fonction de traitement pour la réponse "PC"
def handle_pc_response(client_socket):
    # Traitement spécifique pour la réponse "PC"
    pass

# Fonction de traitement pour la réponse "LED"
def handle_led_response(client_socket):
    # Traitement spécifique pour la réponse "LED"
    pass

# Fonction de traitement pour les informations de rendez-vous
def handle_appointment_info(message, client_socket):
    # Traitement spécifique pour les informations de rendez-vous
    pass

# Fonction de traitement pour faire un choix
def handle_make_choice(message, client_socket):
    # Traitement spécifique pour faire un choix
    pass

# Fonction de traitement pour un booléen
def handle_boolean(message, client_socket):
    # Traitement spécifique pour un booléen
    pass

# Fonction de traitement pour les informations de rappel
def handle_reminder_info(message, client_socket):
    # Traitement spécifique pour les informations de rappel
    pass

# Définition des comportements personnalisés pour les réponses
server.pc_response_handler = handle_pc_response
server.led_response_handler = handle_led_response

# Définition des gestionnaires d'état personnalisés
server.appointment_info_state_handler = handle_appointment_info
server.make_choice_state_handler = handle_make_choice
server.boolean_state_handler = handle_boolean
server.reminder_info_state_handler = handle_reminder_info

# Démarrage du serveur WebSocket
server.start()
while True:
    server.handle_clients()
    pass