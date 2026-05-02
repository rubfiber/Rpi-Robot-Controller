from .Controller import PiController
import time

class UltrasonicSensor:
    def __init__(self, trig: int, echo: int, controller: PiController, name="defaultSensor"):
        self.trig = trig
        self.echo = echo
        self.controller = controller
        self.name = name
        self.controller.add_digital_output(name + "trigger", trig)
        self.controller.add_digital_input(name + "echo", echo)

    def runDistanceLoop(self, pulse=0.00001, interval=0.1):
        self.controller.write_digital(self.name + "trigger", 1)
        time.sleep(pulse)  # 10 microsecond pulse
        self.controller.write_digital(self.name + "trigger", 0)

        # 2. Capture start and end times (Synchronous/Blocking)
        # Note: We keep these loops tight for accuracy
        pulse_start = time.time()
        pulse_end = time.time()

        while self.controller.read_digital(self.name + "echo") == 0:
            pulse_start = time.time()
            
        while self.controller.read_digital(self.name + "echo") == 1:
            pulse_end = time.time()

        # 3. Calculate distance
        duration = pulse_end - pulse_start
        distance = round(duration * 17150, 2)  # Speed of sound (343m/s) / 2

        time.sleep(interval)
        return distance
    