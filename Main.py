#!/usr/bin/python3
from src.main.Controller import PiController
from signal import signal, SIGTERM, SIGHUP
from src.main.DCMotor import DCMotor
from src.main.L293D import L293D
from src.main.UltrasonicSensor import UltrasonicSensor
from src.main.SG90Servo import Servo180Degree as Servo
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
    MotorController = L293D(13, 17, 12, 11, 9, 10, controller, "L293D")
    Motor = DCMotor(MotorController, 0, controller)

    controller.add_pwm_output("LED", 16)
    us = UltrasonicSensor(24, 23, controller=controller)

    servo = Servo(16, controller =controller, name="myServo")
    try:
     Motor.setPower(0.1)
     while True:
            Motor.setPower(1)
            sleep(2)
            Motor.setPower(0)   # stop first
            sleep(0.5)      # let it come to a stop
            Motor.setPower(-1)
            sleep(2)
            Motor.setPower(0)
            sleep(0.5)
    except KeyboardInterrupt:
        safe_exit(None, None)