import RPi.GPIO as GPIO
import time

class PushButton:
    def __init__(self, pin=26, pull_up_down=GPIO.PUD_UP):
        """
        Initialize the push button
        
        Args:
            pin (int): GPIO pin number (default: 26)
            pull_up_down: Pull up/down resistor setting (default: GPIO.PUD_UP)
        """
        self.pin = pin
        self.pull_up_down = pull_up_down
        self._setup()
    
    def _setup(self):
        """Configure the GPIO pin for the button"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=self.pull_up_down)
    
    def is_button_pushed(self):
        """
        Check if the button is currently pressed
        
        Returns:
            bool: True if button is pressed, False otherwise
        """
        return GPIO.input(self.pin) == GPIO.LOW
    
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()
