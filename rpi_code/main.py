import time
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from laser_sensor import LaserSensor


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

        while True:
            laser_sensor.wait_for_beam_break()
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

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        sorter.cleanup()
        laser_sensor.cleanup()

"""
        while True:
            # Wait for user input from the console
            # user_input = input("Enter command: ").strip().lower()
            laser_sensor.wait_for_beam_break()
            predicted_label = identifier.capture_image()
            
            if user_input == 'q':
                print("Exiting program.")
                break
            elif user_input == 'c':
                print("im here after c note")
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
            else:
                print("Invalid command. Please type 'c' or 'q'.")

    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        
    finally:
        # Clean up GPIO resources
        sorter.cleanup()
"""
if __name__ == "__main__":
    main()
