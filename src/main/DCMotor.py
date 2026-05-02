from .Controller import PiController
from .L293D import L293D

class DCMotor:
    def __init__(self, HBridge: L293D, motor_0_or_1: int, controller: PiController): 
        """motor 0 or 1 - what pins ont the H-bridge is the motor connected to? refer to its pinout if unsure."""
        self.HBridge = HBridge
        self.motor = motor_0_or_1
        self.controller = controller

    def setPower(self, power):
        self.HBridge.directionalControl(self.motor, power)
    def brake(self):
        if self.motor == 0:
            self.controller.write_digital("input 1", 0)
            self.controller.write_digital("input 2", 0)
        else:
            self.controller.write_digital("input 3", 0)
            self.controller.write_digital("input 4", 0)