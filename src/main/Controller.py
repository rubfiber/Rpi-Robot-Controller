#!/usr/bin/python3
"""
Template:       Raspberry Pi Analog/Digital Hardware Controller (lgpio version)
Description:    A reusable template for reading and writing to hardware on a 
                Raspberry Pi using lgpio. This is compatible with newer Pi 
                hardware and OS versions.
"""

import lgpio
from smbus import SMBus
from signal import signal, SIGTERM, SIGHUP
from time import sleep

class PiController:
    def __init__(self, i2c_bus=1, adc_address=0x4b):
        """Initialize the controller, I2C bus, and GPIO chip handle."""
        # Setup I2C for the ADS7830
        try:
            self.bus = SMBus(i2c_bus)
        except FileNotFoundError:
            print(f"Warning: I2C bus {i2c_bus} not found. Analog reads will fail.")
            self.bus = None
            
        self.adc_address = adc_address
        self.ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

        # Setup lgpio chip handle (0 is usually the main GPIO header)
        self.chip = lgpio.gpiochip_open(0)
        self.devices = {} # Stores pin configuration info

    # ------------------------------------------------------------------------
    # DEVICE REGISTRATION
    # ------------------------------------------------------------------------
    def add_digital_input(self, name, pin, pull_up=False):
        """Register a digital input pin."""
        # Use SET_PULL_UP or SET_PULL_DOWN if needed
        flags = lgpio.SET_PULL_UP if pull_up else lgpio.SET_PULL_DOWN
        lgpio.gpio_claim_input(self.chip, pin, flags)
        self.devices[name] = {"pin": pin, "type": "input"}

    def add_digital_output(self, name, pin):
        """Register a standard digital output pin."""
        lgpio.gpio_claim_output(self.chip, pin)
        self.devices[name] = {"pin": pin, "type": "output"}

    def add_pwm_output(self, name, pin, frequency=1000):
        """to register motors, leds, etc"""
        lgpio.gpio_claim_output(self.chip, pin)
        self.devices[name] = {"pin": pin, "type": "pwm", "freq": frequency}

    # ------------------------------------------------------------------------
    # READING FUNCTIONS
    # ------------------------------------------------------------------------
    def read_analog(self, channel):
        """Read 0-255 from the ADS7830 ADC on given channel."""
        if self.bus is None: return 0
        if not (0 <= channel <= 7):
            raise ValueError("ADS7830 channel must be 0-7")
        
        self.bus.write_byte(self.adc_address, self.ads7830_commands[channel])
        return self.bus.read_byte(self.adc_address)

    def read_digital(self, name):
        """Read state of a digital input (Returns 1 for High, 0 for Low)."""
        pin = self.devices[name]["pin"]
        return lgpio.gpio_read(self.chip, pin)

    # ------------------------------------------------------------------------
    # WRITING FUNCTIONS
    # ------------------------------------------------------------------------
    def write_digital(self, name, state: bool):
        """Turn a digital output High or Low."""
        pin = self.devices[name]["pin"]
        lgpio.gpio_write(self.chip, pin, int(state))

    def write_analog_pwm(self, name, duty_cycle):
        """
        Write PWM using a scale from 0.0 (off) to 1.0 (full brightness/speed).
        """
        if name not in self.devices or self.devices[name]["type"] != "pwm":
            print(f"Error: {name} is not registered as a PWM output.")
            return

        device = self.devices[name]
        pin = device["pin"]
        freq = device["freq"]
        
        # Clamp input between 0.0 and 1.0 to ensure safety
        val_0_to_1 = max(0.0, min(1.0, float(duty_cycle)))
        
        # Convert 0.0-1.0 scale to 0-100 percentage for lgpio
        percentage = val_0_to_1 * 100
        lgpio.tx_pwm(self.chip, pin, freq, percentage)
    # ------------------------------------------------------------------------
    # HELPER FUNCTIONS
    # ------------------------------------------------------------------------
    @staticmethod
    def map_value(value, in_min, in_max, out_min, out_max):
        if in_max == in_min: return out_min 
        mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return max(out_min, min(out_max, mapped))

    def apply_joystick_deadzone(self, value, center=127, deadzone=15):
        if (center - deadzone) < value < (center + deadzone):
            return center
        return value

    # ------------------------------------------------------------------------
    # CLEANUP
    # ------------------------------------------------------------------------
    def cleanup(self):
        print("Cleaning up GPIO...")
        for name, info in self.devices.items():
            try:
                if info["type"] == "pwm":
                    lgpio.tx_pwm(self.chip, info["pin"], 1, 0)
                lgpio.gpio_free(self.chip, info["pin"])
            except Exception:
                pass
        lgpio.gpiochip_close(self.chip)
