from myassistant import MyAssistant


my_assistant = MyAssistant(model='tiny', commands_callback=print,
                           n_threads=3, input_device=0, q_threshold=4)
# print(Assistant.available_devices)
my_assistant.start()
