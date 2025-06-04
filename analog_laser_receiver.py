import spidev
import time
import RPi.GPIO as GPIO

class AnalogLaserReceiver:
    def __init__(self, laser_pin=17):  # Default laser pin is GPIO 17
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, CE0 (GPIO 8)
        self.spi.max_speed_hz = 1000000  # 1MHz
        
        # Set up GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(8, GPIO.OUT)  # CE0
        GPIO.setup(9, GPIO.IN)   # MISO
        GPIO.setup(10, GPIO.OUT) # MOSI
        GPIO.setup(11, GPIO.OUT) # SCLK
        
        # Set up laser pin
        self.laser_pin = laser_pin
        GPIO.setup(self.laser_pin, GPIO.OUT)
        self.laser_on = False

    def turn_laser_on(self):
        GPIO.output(self.laser_pin, GPIO.HIGH)
        self.laser_on = True

    def turn_laser_off(self):
        GPIO.output(self.laser_pin, GPIO.LOW)
        self.laser_on = False

    def read_value(self):
        # Read analog value from MCP3008 channel 0
        # Command format: [start bit, single-ended bit, channel select, don't care bits]
        cmd = 0x80  # 1000 0000 - start bit + single-ended + channel 0
        resp = self.spi.xfer2([cmd, 0x00, 0x00])
        
        # Combine the response bytes into a 10-bit value
        value = ((resp[1] & 0x03) << 8) + resp[2]
        return value

    def cleanup(self):
        self.turn_laser_off()  # Make sure laser is off before cleanup
        self.spi.close()
        GPIO.cleanup()

def main():
    try:
        # Create instance of AnalogLaserReceiver
        laser_receiver = AnalogLaserReceiver()
        
        # Threshold for laser detection (adjust as needed)
        THRESHOLD = 500
        
        print("Starting laser detection...")
        print("Turning laser ON...")
        laser_receiver.turn_laser_on()
        
        while True:
            value = laser_receiver.read_value()
            if value < THRESHOLD:
                print("Laser beam detected")
            else:
                print("No laser beam")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        laser_receiver.cleanup()

if __name__ == "__main__":
    main() 