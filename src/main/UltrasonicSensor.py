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

    def runDistanceLoop(self, pulse=0.00001, interval=0.1, timeout=0.1):
        self.controller.write_digital(self.name + "trigger", 1)
        time.sleep(pulse)
        self.controller.write_digital(self.name + "trigger", 0)

        deadline = time.time() + timeout
        pulse_start = None
        pulse_end = None

        while self.controller.read_digital(self.name + "echo") == 0:
            if time.time() > deadline:
                print("DEBUG: timed out waiting for echo HIGH")  # stuck here?
                return None
            pulse_start = time.time()


        while self.controller.read_digital(self.name + "echo") == 1:
            if time.time() > deadline:
                print("DEBUG: timed out waiting for echo LOW")  # or here?
                return None
            pulse_end = time.time()


        if pulse_start is None or pulse_end is None:
            return None

        duration = pulse_end - pulse_start
        distance = round(duration * 17150, 2)
        time.sleep(interval)
        return distance