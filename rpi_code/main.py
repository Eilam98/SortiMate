import time
from sorting_mechanism import SortingMechanism, WasteType

def main():
    try:
        sorter = SortingMechanism(rotation_pin=17, gate_pin=27) # GPIO17 for rotation servo, GPIO27 for gate servo
        print("Smart Recycling Bin initialized...")

        sorter.gate_servo.set_angle(90)
        time.sleep(2)
        sorter.gate_servo.set_angle(0)
        time.sleep(2)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up GPIO resources
        sorter.cleanup()

if __name__ == "__main__":
    main()