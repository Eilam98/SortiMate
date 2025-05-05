import RPi.GPIO as GPIO
import time

# Pin setup
LASER_PIN = 17  # Connects to KY-008 'S' pin
SENSOR_PIN = 27  # Connects to Receiver 'DO' pin

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)

print("Starting laser test. Press Ctrl+C to stop.")

try:
    GPIO.output(LASER_PIN, GPIO.HIGH)  # Turn ON laser
    while True:
        sensor_value = GPIO.input(SENSOR_PIN)
        if sensor_value == GPIO.LOW:
            print("✅ Laser beam detected.")
        else:
            print("❌ No beam detected.")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Test stopped by user.")

finally:
    GPIO.output(LASER_PIN, GPIO.LOW)  # Turn OFF laser
    GPIO.cleanup()
