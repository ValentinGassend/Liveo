import time
from Myassistant import MyAssistant

def run_assistant():
    # Créez une instance de l'assistant
    assistant = MyAssistant()

    # Démarrez l'assistant
    print("Démarrage de l'assistant...")
    assistant.start()

    # Attendez un retour
    print("Attente d'un retour pendant 5 secondes...")
    time.sleep(5)

    # Arrêtez l'assistant
    print("Arrêt de l'assistant...")
    assistant.close()

    # Attendez 5 secondes
    print("Attente de 5 secondes...")
    time.sleep(5)

    # Redémarrez l'assistant
    print("Redémarrage de l'assistant...")
    assistant.start()

run_assistant()
