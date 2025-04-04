"""
Servo motor controller class for managing servo motor operations.
This module provides a base class for controlling servo motors using the RPi.GPIO library.
"""

import RPi.GPIO as GPIO
import time
from typing import Optional

class ServoController:
    
    def __init__(self, pin: int, frequency: int = 50, min_duty_cycle: float = 2.5, max_duty_cycle: float = 12.5):
        """
        Initialize the servo controller.
        
        """ 
        self.pin = pin
        self.frequency = frequency
        self.min_duty_cycle = min_duty_cycle
        self.max_duty_cycle = max_duty_cycle
        self.current_angle = 0
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)
    
    def set_angle(self, angle: float) -> None:
        """
        Set the servo motor to a specific angle.

        """
    
        if not 0 <= angle <= 180:
            raise ValueError("Angle must be between 0 and 180 degrees")
        
        # Convert angle to duty cycle
        duty_cycle = self.min_duty_cycle + (angle / 180) * (self.max_duty_cycle - self.min_duty_cycle)
        self.pwm.ChangeDutyCycle(duty_cycle)
        self.current_angle = angle
        time.sleep(0.3)  # Give servo time to move
    
    def get_current_angle(self) -> float:
        """
        Get the current angle of the servo.

        """
        return self.current_angle
    
    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        self.pwm.stop()
        GPIO.cleanup() 
