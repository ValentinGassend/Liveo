from Myassistant import MyAssistant

def MyCustomFunction(data):
    print("passed by My Custom Function "+data)
    my_assistant.close()
my_assistant = MyAssistant(model='medium', commands_callback=MyCustomFunction,
                           n_threads=12, input_device=0, q_threshold=6, silence_threshold=50)


# print(Assistant.available_devices)
my_assistant.start()

while True:
    pass