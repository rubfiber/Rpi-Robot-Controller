from .Controller import PiController

class GenericAnalogSensor:

    def __init__(self, pin: int, controller: PiController, name="defaultAnalogSensor"):
        """The pin here is the pin on the ADS 7830. Don't connect it to the RPi directly."""
        self.pin = pin
        self.controller = controller
        self.name = name
        self.controller.add_analog_input(name, pin)

    def read(self):
        return self.controller.read_analog(self.name)