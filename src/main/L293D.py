from .Controller import PiController
class L293D:
    
    def __init__(self, enable12: int, in1: int, in2: int, enable34, in3: int, 
                 in4: int, controller: PiController, name="defaultMotorController"):
        self.enable12 = enable12
        self.enable34 = enable34
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4
        self.controller = controller
        self.name = name
        controller.add_pwm_output(name+"1", enable12)
        controller.add_pwm_output(name+"2", enable34)

        controller.add_digital_output("input 1", in1)
        controller.add_digital_output("input 2", in2)
        controller.add_digital_output("input 3", in3)
        controller.add_digital_output("input 4", in4)
        
        self.dirmotor1 = {
                          "enable": enable12, 
                          "input1": in1, 
                          "input2": in2, 
                          }
        self.dirmotor2 = {
                          "enable": enable34, 
                          "input1": in3, 
                          "input2": in4, 
                          }
        self.motor1 = {
                        "enable": enable12, 
                        "input": in1, 
                        }
        self.motor2 = {
                        "enable": enable12, 
                        "input": in2, 
                        }
        self.motor3 = {
                        "enable": enable34, 
                        "input": in3, 
                        }
        self.motor4 = {
                        "enable": enable34, 
                        "input": in4, 
                        }
    def directionalControl(self, motor: int, power):
      if motor == 0:
          input1_name = "input 1"
          input2_name = "input 2"
          enable_name = self.name + "1"
      else:
          input1_name = "input 3"
          input2_name = "input 4"
          enable_name = self.name + "2"

      if power >= 0:
          self.controller.write_digital(input1_name, 1)
          self.controller.write_digital(input2_name, 0)
      else:
          self.controller.write_digital(input1_name, 0)
          self.controller.write_digital(input2_name, 1)

      self.controller.write_analog_pwm(enable_name, abs(power))
      #  def quadControl(motor:dict, power):
        #    if motor.enable == self.enable12:
         #      if power >= 0:
                  