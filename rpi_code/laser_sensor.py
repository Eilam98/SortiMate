import RPi.GPIO as GPIO
import time

class LaserSensor:
    def __init__(self, laser_pin: int, receiver_pin: int):
        self.laser_pin = laser_pin
        self.receiver_pin = receiver_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser_pin, GPIO.OUT)
        GPIO.setup(self.receiver_pin, GPIO.IN)

        GPIO.output(self.laser_pin, GPIO.HIGH)  # Turn laser ON

    def is_beam_broken(self) -> bool:
        """
        Returns True if the laser beam is interrupted (e.g., object detected).
        """
        return GPIO.input(self.receiver_pin) == GPIO.HIGH  # Depending on module logic level

    def wait_for_beam_break(self):
        """
        Blocks until the laser beam is broken.
        """
        print("Waiting for object to break the laser beam...")
        while not self.is_beam_broken():
            time.sleep(0.05)
        print("Beam broken detected!")

    def cleanup(self):
        GPIO.output(self.laser_pin, GPIO.LOW)
        GPIO.cleanup([self.laser_pin, self.receiver_pin])
