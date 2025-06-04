import spidev
import time
import RPi.GPIO as GPIO

def test_basic_spi():
    # Initialize SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Bus 0, CE0
    spi.max_speed_hz = 100000  # 100kHz
    spi.mode = 0

    print("Starting Basic SPI test...")
    print("----------------------------------------")

    try:
        # Simple loopback test
        print("\nPerforming loopback test...")
        print("Connect MOSI (GPIO 10) to MISO (GPIO 9) for this test")
        print("Press Enter when ready...")
        input()

        test_data = [0x55, 0xAA, 0xFF]  # 01010101, 10101010, 11111111
        for data in test_data:
            resp = spi.xfer2([data])
            print(f"Sent: {hex(data)} ({bin(data)[2:].zfill(8)}), Received: {hex(resp[0])} ({bin(resp[0])[2:].zfill(8)})")
            time.sleep(0.5)

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        spi.close()
        print("\nTest complete")

if __name__ == "__main__":
    test_basic_spi() 