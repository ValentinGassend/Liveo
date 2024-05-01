my_button = Button(23)
button_status = False

while True:
    if not button_status:
        button_status = my_button.check_status()
    else:
        print("Appui long détecté")
        # Effectuer les actions souhaitées pour l'appui long
        # ...
        my_button.reset()
        button_status = False