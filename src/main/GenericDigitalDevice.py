from .Controller import PiController

class GenericDigitalDevice:
    def __init__(self, pin: int, controller: PiController, name="defaultDevice"):
        self.pin = pin
        self.controller = controller
        self.name = name
        self.controller.add_digital_output(name, pin)

    def setState(self, state: bool):
        self.controller.write_digital(self.name, 1 if state else 0)