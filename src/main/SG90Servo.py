from .Controller import PiController
import time

class Servo180Degree:
    def __init__(self, pin: int, controller: PiController, name="defaultServo"):
        self.pin = pin
        self.controller = controller
        self.name = name
        self.controller.add_pwm_output(name, pin, frequency=50)  # 50Hz for SG90

    def setPosition(self, angle):
        if not (0 <= angle <= 180):
            raise ValueError("Angle must be between 0 and 180")
        duty_cycle = (angle / 18) + 2.5
        self.controller.write_analog_pwm(self.name, duty_cycle / 100)
        
    def sweep(self, step=1, delay=0.05):
        while True:
            for angle in range(0, 181, step):
                self.setPosition(angle)
                time.sleep(delay)
            for angle in range(180, -1, -step):
                self.setPosition(angle)
                time.sleep(delay)