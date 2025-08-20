import time
import os
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback
from monitor_manager import MonitorManager

def main():
    try:
        sorter = SortingMechanism(rotation_pin=27, gate_pin=22) # TO EDIT: GPIO17 for rotation servo, GPIO27 for gate servo
        identifier = CameraManager()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # get the directory where main.py lives
        IMG  = os.path.join(BASE_DIR, "monitor_images")
        image_dirs = {
            "default":      os.path.join(IMG, "default.png"),
            "classifying":  os.path.join(IMG, "classifying.png"),
            "Plastic":      os.path.join(IMG, "plastic.png"),
            "Glass":        os.path.join(IMG, "glass.png"),
            "Metal":        os.path.join(IMG, "metal.png"),
            "Other":        os.path.join(IMG, "other.png"),
            "summary":      os.path.join(IMG, "summary.png"),
        }
        monitor = MonitorManager(
            images_dir=image_dirs,
            window_size=(1920, 1080),
            display=":0.0",
            monitor_index=1  # Explicitly set to HDMI-2
        )
        monitor.show("default")

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
                monitor.show("classifying")
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
                monitor.show(predicted_label)
                print(f"Sorting waste of type: {predicted_label}")
                time.sleep(5)
                sorter.sort_waste(waste_type)
                monitor.show("summary")
                time.sleep(5)
                monitor.show("default")
                
            else:
                print("Invalid command. Please type 'c' or 'q'.")
        time.sleep(1)

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
