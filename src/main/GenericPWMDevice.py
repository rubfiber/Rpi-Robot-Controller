from .Controller import PiController
class GenericPWMDevice:
    def __init__(self, pin: int, controller: PiController, name="defaultPWMDevice", frequency=50):
        self.pin = pin
        self.controller = controller
        self.name = name
        self.controller.add_pwm_output(name, pin, frequency=frequency)
    def setPWMValue(self, duty_cycle):
        assert 0.0 <= duty_cycle <= 1.0, "Duty cycle must be between 0.0 and 1.0 - if using 0-100, divide the value by 100 first before passng it in"
        """
        Set the duty cycle for the PWM device using a scale from 0.0 (off) to 1.0 (full power).
        """
        self.controller.write_analog_pwm(self.name, duty_cycle)