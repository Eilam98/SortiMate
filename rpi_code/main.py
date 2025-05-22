import time
import os
import threading
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from monitor_manager import MonitorManager

def main():
    try:
        sorter = SortingMechanism(rotation_pin=27, gate_pin=22) # TO EDIT: GPIO17 for rotation servo, GPIO27 for gate servo
        identifier = CameraManager()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # get the directory where main.py lives
        monitor = MonitorManager(
            image_dirs = {
                "default":      [os.path.join(BASE_DIR, "monitor_images", "default1.png"),
                                os.path.join(BASE_DIR, "monitor_images", "default2.jpeg")],
                "classifying":  [os.path.join(BASE_DIR, "monitor_images", "classify1.gif"),
                                os.path.join(BASE_DIR, "monitor_images", "classify2.gif")],
                "plastic":      [os.path.join(BASE_DIR, "monitor_images", "plastic.jpeg")],
                "glass":        [os.path.join(BASE_DIR, "monitor_images", "glass.jpeg")],
                "metal":        [os.path.join(BASE_DIR, "monitor_images", "metal.jpeg")],
                "other":        [os.path.join(BASE_DIR, "monitor_images", "other.jpeg")],
                "summary":      [os.path.join(BASE_DIR, "monitor_images", "summary.jpeg")],
            },
            interval=3.0,             # change every 3 seconds
            window_size=(1920, 1080),  # match your monitor resolution
            display=":0.1"
        )
        monitor.start()
        print("Smart Recycling Bin initialized...")
        
        print("Type 'c' (then press Enter) to capture an image for classification.")
        print("Type 'q' (then Enter) to exit the program.")

        while True:
            # Wait for user input from the console
            user_input = input("Enter command: ").strip().lower()

            if user_input == 'q':
                print("Exiting program.")
                break
            elif user_input == 'c':
                print("im here after c note")
                monitor.set_state("classifying")
                predicted_label = identifier.capture_image()
                if predicted_label == "Plastic":
                    waste_type = WasteType.PLASTIC
                elif predicted_label == "Glass":
                    waste_type = WasteType.GLASS
                elif predicted_label == "Metal":
                    waste_type = WasteType.METAL
                else:
                    waste_type = WasteType.OTHER
                    predicted_label = "Other"
                monitor.set_state(predicted_label)
                print(f"Sorting waste of type: {predicted_label}")
                sorter.sort_waste(waste_type)
                monitor.set_state("summary")
                # schedule a switch back to default in 5 s, without blocking the program
                threading.Timer(5.0, lambda: monitor.set_state("default")).start()
            else:
                print("Invalid command. Please type 'c' or 'q'.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        
    finally:
        # clean up both monitor and GPIO
        monitor.stop()
        sorter.cleanup()

if __name__ == "__main__":
    main()
