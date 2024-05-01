from btn import Btn

button_pin = 10
my_btn = Btn(button_pin)

while True:
    my_btn.checking_state()
    button_state = my_btn.pressed

    # Faites quelque chose avec l'état du bouton (button_state) ici
    # Par exemple, vous pouvez l'afficher à la console ou effectuer une action en fonction de son état
    if button_state:
        print("Le bouton est pressé")
    else:
        print("Le bouton n'est pas pressé")
