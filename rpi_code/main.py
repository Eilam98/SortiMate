import time
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from laser_sensor import LaserSensor


def main():
    try:
        # Initialize components
        sorter = SortingMechanism(rotation_pin=27, gate_pin=22)
        identifier = CameraManager()
        laser_sensor = LaserSensor(laser_pin=23, threshold=500)  # Using default threshold of 500
        
        print("Smart Recycling Bin initialized...")
        print("Waiting for object to enter the bin...")

        while True:
            # Wait for beam to be broken
            while not laser_sensor.is_beam_broken():
                time.sleep(0.1)
            
            print("Object detected!")
            predicted_label = identifier.capture_image()

            if predicted_label == "Plastic":
                waste_type = WasteType.PLASTIC
            elif predicted_label == "Glass":
                waste_type = WasteType.GLASS
            elif predicted_label == "Metal":
                waste_type = WasteType.METAL
            else:
                waste_type = WasteType.OTHER

            print(f"Sorting waste of type: {predicted_label}")
            sorter.sort_waste(waste_type)

            # Wait until beam is restored before detecting the next object
            while laser_sensor.is_beam_broken():
                time.sleep(0.1)
            
            print("Object sorted. Waiting for next object...")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        # Clean up resources
        sorter.cleanup()
        laser_sensor.cleanup()


if __name__ == "__main__":
    main()
