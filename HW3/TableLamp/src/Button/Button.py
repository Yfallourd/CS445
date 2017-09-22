class Button:
    def __init__(self, lightbulb):
        self._lightbulb = lightbulb

    def switchOn(self):
        print("Button switched to ON")
        self._lightbulb.on()

    def switchOff(self):
        print("Button switched to OFF")
        self._lightbulb.off()
