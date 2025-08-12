import spidev
import time
import RPi.GPIO as GPIO

def test_spi():
    # Initialize SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Bus 0, CE0
    spi.max_speed_hz = 100000  # 100kHz
    spi.mode = 0

    # Set up GPIO for CS
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(8, GPIO.OUT)  # CE0
    GPIO.output(8, GPIO.HIGH)  # CS active low, so start high

    print("Starting Combined SPI test...")
    print("----------------------------------------")

    try:
        # Test 1: Simple MCP3008 read
        print("\nTest 1: Simple MCP3008 read")
        for channel in range(8):
            cmd = 0x80 | ((channel & 0x07) << 4)  # 1000 0000 + channel bits
            GPIO.output(8, GPIO.LOW)  # Activate CS
            time.sleep(0.0001)
            resp = spi.xfer2([cmd, 0x00, 0x00])
            GPIO.output(8, GPIO.HIGH)  # Deactivate CS
            value = ((resp[1] & 0x03) << 8) + resp[2]
            print(f"Channel {channel} - Raw: {[hex(x) for x in resp]}, Value: {value}")

        # Test 2: Continuous reading from channel 0
        print("\nTest 2: Continuous reading from channel 0")
        print("Reading for 5 seconds...")
        start_time = time.time()
        while time.time() - start_time < 5:
            GPIO.output(8, GPIO.LOW)  # Activate CS
            time.sleep(0.0001)
            resp = spi.xfer2([0x80, 0x00, 0x00])  # Read channel 0
            GPIO.output(8, GPIO.HIGH)  # Deactivate CS
            value = ((resp[1] & 0x03) << 8) + resp[2]
            print(f"Raw: {[hex(x) for x in resp]}, Value: {value}")
            time.sleep(0.5)

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        spi.close()
        GPIO.cleanup()
        print("\nTest complete")

if __name__ == "__main__":
    test_spi() 