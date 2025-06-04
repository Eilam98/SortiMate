import spidev
import time
import RPi.GPIO as GPIO
import atexit

class AnalogLaserReceiver:
    def __init__(self, laser_pin=23):  # Default laser pin is GPIO 23
        # Disable GPIO warnings
        GPIO.setwarnings(False)
        
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, CE0 (GPIO 8)
        self.spi.max_speed_hz = 100000  # 100kHz
        self.spi.mode = 0  # Set SPI mode 0
        
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
        
        # Initialize CS pin
        GPIO.output(8, GPIO.HIGH)  # CS active low, so start high
        
        # Register cleanup function
        atexit.register(self.cleanup)
        
        # Test ADC connection
        print("Testing ADC connection...")
        self.test_adc()

    def test_adc(self):
        """Test ADC connection by reading all channels"""
        print("\nTesting all ADC channels:")
        for channel in range(8):
            value = self.read_adc_channel(channel)
            print(f"Channel {channel}: {value}")
        print("ADC test complete\n")

    def read_adc_channel(self, channel):
        """Read a specific ADC channel"""
        # Command format: [start bit, single-ended bit, channel select, don't care bits]
        cmd = 0x80 | ((channel & 0x07) << 4)  # 1000 0000 + channel bits
        
        # Activate CS
        GPIO.output(8, GPIO.LOW)
        time.sleep(0.0001)  # Small delay for stability
        
        try:
            # Send command and read response - using the same approach as spi_test.py
            resp = self.spi.xfer2([cmd, 0x00, 0x00])
            
            # Debug print for troubleshooting
            print(f"Channel {channel} raw response: {[hex(x) for x in resp]}")
            
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
        # Read analog value from MCP3008 channel 0
        value = self.read_adc_channel(0)
        
        # Debug print
        print(f"ADC Channel 0 value: {value}")
        
        return value

    def turn_laser_on(self):
        print("Turning laser ON...")
        GPIO.output(self.laser_pin, GPIO.HIGH)
        self.laser_on = True
        # Verify laser state
        if GPIO.input(self.laser_pin) == GPIO.HIGH:
            print("Laser pin is HIGH")
        else:
            print("WARNING: Laser pin is not HIGH!")

    def turn_laser_off(self):
        print("Turning laser OFF...")
        GPIO.output(self.laser_pin, GPIO.LOW)
        self.laser_on = False

    def cleanup(self):
        """Clean up GPIO and SPI resources"""
        try:
            self.turn_laser_off()  # Make sure laser is off
            if hasattr(self, 'spi'):
                self.spi.close()
            GPIO.cleanup()
            print("Resources cleaned up successfully")
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main():
    try:
        # Create instance of AnalogLaserReceiver
        laser_receiver = AnalogLaserReceiver()
        
        # Threshold for laser detection (adjust as needed)
        THRESHOLD = 500
        
        print("\nStarting laser detection...")
        print("Turning laser ON...")
        laser_receiver.turn_laser_on()
        
        # Test laser state
        print(f"Laser pin state: {'HIGH' if GPIO.input(laser_receiver.laser_pin) == GPIO.HIGH else 'LOW'}")
        
        print("\nStarting continuous monitoring...")
        print("Press Ctrl+C to exit")
        print("----------------------------------------")
        
        # First, read all channels to see their values
        print("\nInitial channel readings:")
        for channel in range(8):
            value = laser_receiver.read_adc_channel(channel)
            print(f"Channel {channel}: {value}")
        print("----------------------------------------")
        
        # Test with laser on and off
        print("\nTesting with laser on and off:")
        print("Laser ON - reading values...")
        for _ in range(3):
            value = laser_receiver.read_value()
            print(f"Value with laser ON: {value}")
            time.sleep(0.5)
        
        print("\nLaser OFF - reading values...")
        laser_receiver.turn_laser_off()
        for _ in range(3):
            value = laser_receiver.read_value()
            print(f"Value with laser OFF: {value}")
            time.sleep(0.5)
        
        print("\nTurning laser back ON for continuous monitoring...")
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
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Cleanup will be handled by atexit handler
        pass

if __name__ == "__main__":
    main() 