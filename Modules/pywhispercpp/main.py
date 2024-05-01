from myassistant import MyAssistant

def MyCustomFunction(data):
    print("passed by My Custom Function "+data)
    my_assistant.close()
my_assistant = MyAssistant(model='tiny', commands_callback=MyCustomFunction,
                           n_threads=3, input_device=0, q_threshold=4)


# print(Assistant.available_devices)
my_assistant.start()

while True:
    pass