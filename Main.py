#!/usr/bin/python3
from src.main.Controller import PiController
from signal import signal, SIGTERM, SIGHUP
from src.main.DCMotor import DCMotor
from src.main.L293D import L293D
from src.main.UltrasonicSensor import UltrasonicSensor
from time import sleep
# ============================================================================
# EXAMPLE USAGE
# ============================================================================
if __name__ == "__main__":
    controller = PiController()

    def safe_exit(signum, frame):
        controller.cleanup()
        exit(0)

    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    # Setup
    #MotorController = L293D(13, 19, 5, 0, 0, 0, controller, "L293D")
    #Motor = DCMotor(MotorController, 0, controller)

    controller.add_pwm_output("LED", 16)
    us = UltrasonicSensor(24, 23  , controller=controller)
        
    try:
       while True:
         dist = us.runDistanceLoop()
         if dist is not None:
            print(dist)
         else:
          print("No reading (timeout)")

    except KeyboardInterrupt:
        safe_exit(None, None)