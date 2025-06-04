import spidev
import time
import RPi.GPIO as GPIO
import atexit

class LaserSensor:
    def __init__(self, laser_pin=23, threshold=500):
        """
        Initialize the laser sensor with specified pins and threshold.
        
        Args:
            laser_pin (int): GPIO pin number for the laser (default: 23)
            threshold (int): Threshold value for beam detection (default: 500)
        """
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        
        # Store parameters
        self.laser_pin = laser_pin
        self.threshold = threshold
        
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, CE0 (GPIO 8)
        self.spi.max_speed_hz = 100000  # 100kHz
        self.spi.mode = 0  # Set SPI mode 0
        
        # Set up GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(8, GPIO.OUT)  # CE0
        GPIO.output(8, GPIO.HIGH)  # CS active low, so start high
        
        # Set up laser pin
        GPIO.setup(self.laser_pin, GPIO.OUT)
        self.laser_on = False
        
        # Register cleanup function
        atexit.register(self.cleanup)
        
        # Turn on the laser
        self.turn_laser_on()

    def read_adc_channel(self, channel):
        """Read a specific ADC channel"""
        # Command format: [start bit, single-ended bit, channel select, don't care bits]
        cmd = 0x80 | ((channel & 0x07) << 4)  # 1000 0000 + channel bits
        
        # Activate CS
        GPIO.output(8, GPIO.LOW)
        time.sleep(0.0001)  # Small delay for stability
        
        try:
            # Send command and read response
            resp = self.spi.xfer2([cmd, 0x00, 0x00])
            
            # Combine the response bytes into a 10-bit value
            value = ((resp[1] & 0x03) << 8) + resp[2]
            return value
        except Exception as e:
            print(f"Error reading channel {channel}: {e}")
            return 0
        finally:
            # Deactivate CS
            GPIO.output(8, GPIO.HIGH)
            time.sleep(0.0001)  # Small delay after CS

    def read_value(self):
        """Read the current value from the laser receiver"""
        return self.read_adc_channel(0)

    def is_beam_broken(self):
        """
        Check if the laser beam is broken.
        
        Returns:
            bool: True if beam is broken (value < threshold), False otherwise
        """
        value = self.read_value()
        return value < self.threshold

    def turn_laser_on(self):
        """Turn on the laser"""
        GPIO.output(self.laser_pin, GPIO.HIGH)
        self.laser_on = True

    def turn_laser_off(self):
        """Turn off the laser"""
        GPIO.output(self.laser_pin, GPIO.LOW)
        self.laser_on = False

    def cleanup(self):
        """Clean up GPIO and SPI resources"""
        try:
            self.turn_laser_off()  # Make sure laser is off
            if hasattr(self, 'spi'):
                self.spi.close()
            GPIO.cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main():
    """Test function for the LaserSensor class"""
    try:
        # Create instance of LaserSensor
        sensor = LaserSensor()
        
        print("Starting laser sensor test...")
        print("Press Ctrl+C to exit")
        print("----------------------------------------")
        
        while True:
            if sensor.is_beam_broken():
                print("Beam broken!")
            else:
                print("Beam intact")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main() 