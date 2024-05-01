
class SingleLed:
    def __init__(self,color):
        self.color = color
    def on(self):
        self.color.on()
    def off(self):
        self.color.off()