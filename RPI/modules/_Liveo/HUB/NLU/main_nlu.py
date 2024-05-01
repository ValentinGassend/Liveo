from nlu import Nlu
nlu = Nlu()
nlu.fit()

# Exemple d'utilisation avec un texte
text = "Je veux prendre un rendez-vous professionnel le 6 mai à 15h"
parsing = nlu.run(text=text, intent="rdv")

# Exemple d'utilisation avec un fichier
file_path = "chemin/vers/le/fichier.txt"
parsing = nlu.run(file=file_path, intent="choice")
