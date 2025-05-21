import RPi.GPIO as GPIO
import time

LASER_GPIO = 17
RECEIVER_GPIO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_GPIO, GPIO.OUT)
GPIO.setup(RECEIVER_GPIO, GPIO.IN)

GPIO.output(LASER_GPIO, GPIO.HIGH)  # Turn laser ON

try:
    while True:
        beam_detected = GPIO.input(RECEIVER_GPIO)
        if beam_detected == GPIO.LOW:
            print("Laser beam hit the sensor.")
        else:
            print("No laser beam detected.")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
