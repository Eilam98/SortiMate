import time
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from laser_sensor import LaserSensor
from firebase_handler import log_waste_event, update_bin_status, create_alert

def main():
    try:
        sorter = SortingMechanism(rotation_pin=27,
                                  gate_pin=22)  # TO EDIT: GPIO17 for rotation servo, GPIO27 for gate servo
        identifier = CameraManager()
        laser_sensor = LaserSensor(laser_pin=23, receiver_pin=24)  # needs to set based on the GPIO pins
        print("Smart Recycling Bin initialized...")

        # print("Type 'c' (then press Enter) to capture an image for classification.")
        # print("Type 'q' (then Enter) to exit the program.")
        print("Smart Recycling Bin initialized...")
        print("Waiting for object to enter the bin...")

        bin_id = "bin_001"
        while True:
            laser_sensor.wait_for_beam_break()

            start_time = time.time()

            predicted_label, confidence = identifier.capture_image()

            latency_ms = int((time.time() - start_time) * 1000)

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
            log_waste_event(bin_id=bin_id, waste_type=predicted_label,latency_ms=latency_ms, confidence=confidence) # we need to handle error message (if condition??)
            # Also, we need to handle the user_id ,is it a primary key or not?
            update_bin_status(bin_id=bin_id, waste_type=predicted_label)
            create_alert(bin_id=bin_id, waste_type=predicted_label)
            # Wait until beam is restored before detecting the next object
            while laser_sensor.is_beam_broken():
                time.sleep(0.1)

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
