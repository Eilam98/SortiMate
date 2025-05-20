import time
from sorting_mechanism import SortingMechanism, WasteType
from rpi_code.Waste_recognition import CameraManager

def main():
    try:
        sorter = SortingMechanism(rotation_pin=27, gate_pin=22) # TO EDIT: GPIO17 for rotation servo, GPIO27 for gate servo
        identifier = CameraManager()
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
                predicted_label = identifier.identify_item()
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
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up GPIO resources
        sorter.cleanup()

if __name__ == "__main__":
    main()
