"""
Servo motor controller class for managing servo motor operations.
This module provides a base class for controlling servo motors using the RPi.GPIO library.
"""

import RPi.GPIO as GPIO
import time
from typing import Optional

class ServoController:
    """
    A class to control servo motors connected to a Raspberry Pi.
    
    Attributes:
        pin (int): The GPIO pin number the servo is connected to
        frequency (int): PWM frequency in Hz (typically 50Hz for servos)
        min_duty_cycle (float): Minimum duty cycle percentage (0-100)
        max_duty_cycle (float): Maximum duty cycle percentage (0-100)
        current_angle (float): Current angle of the servo (0-180)
    """
    
    def __init__(self, pin: int, frequency: int = 50, min_duty_cycle: float = 2.5, max_duty_cycle: float = 12.5):
        """
        Initialize the servo controller.
        
        Args:
            pin (int): GPIO pin number
            frequency (int): PWM frequency in Hz
            min_duty_cycle (float): Minimum duty cycle percentage
            max_duty_cycle (float): Maximum duty cycle percentage
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
        
        Args:
            angle (float): Target angle (0-180 degrees)
            
        Raises:
            ValueError: If angle is outside valid range
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
        
        Returns:
            float: Current angle (0-180 degrees)
        """
        return self.current_angle
    
    def cleanup(self) -> None:
        """Clean up GPIO resources."""
        self.pwm.stop()
        GPIO.cleanup() 