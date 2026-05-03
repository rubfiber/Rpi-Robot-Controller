from .Controller import PiController
class GenericDigitalSensor:
    def __init__(self, pin: int, controller: PiController, name="defaultDigitalSensor"):
        self.pin = pin
        self.controller = controller
        self.name = name
        self.controller.add_digital_input(name, pin)

    def read(self):
        return self.controller.read_digital(self.name)