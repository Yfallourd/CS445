class PushButton:

    def __init__(self, lightbulb):
        self._lightbulb = lightbulb
        self.on = False

    def PushButton(self):
        if self.on:
            print("Button switched to OFF")
            self.on = not self.on
            self._lightbulb.off()
        else:
            print("Button switched to ON")
            self.on = not self.on
            self._lightbulb.on()
