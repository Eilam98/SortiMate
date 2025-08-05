import time
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from laser_sensor import LaserSensor


def main():
    try:
        sorter = SortingMechanism(rotation_pin=17, gate_pin=27)
        identifier = CameraManager()
        laser_sensor = LaserSensor(laser_pin=23)
        
        print("Smart Recycling Bin initialized...")
        print("Waiting for object to enter the bin...")

        while True:
            while not laser_sensor.is_beam_broken():
                time.sleep(0.1)
            
            print("New item detected!")
            predicted_label, confidence = identifier.capture_image()

            if predicted_label == "Plastic" and confidence > 0.8:
                waste_type = WasteType.PLASTIC
            elif predicted_label == "Glass"  and confidence > 0.8:
                waste_type = WasteType.GLASS
            elif predicted_label == "Metal" and confidence > 0.8:
                waste_type = WasteType.METAL
            else:
                waste_type = WasteType.OTHER

            print(f"Sorting waste of type: {predicted_label}")
            print("With confidence: ", confidence, "\n")
            sorter.sort_waste(waste_type)

            identifier.upload_image_to_drive(predicted_label, confidence)

            # Wait until beam is restored before detecting the next object
            while laser_sensor.is_beam_broken():
                time.sleep(0.1)
            
            print("Item sorted. Waiting for the next item...")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        sorter.cleanup()
        laser_sensor.cleanup()


if __name__ == "__main__":
    main()
