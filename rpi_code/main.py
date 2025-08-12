# import time
import argparse  # For test mode
# import traceback  # For error handling and testing
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
import traceback


# from laser_sensor import LaserSensors


def label_to_waste_type(label: str) -> WasteType:
    if label == "Plastic":
        return WasteType.PLASTIC
    elif label == "Glass":
        return WasteType.GLASS
    elif label == "Metal":
        return WasteType.METAL
    else:
        return WasteType.OTHER


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-image", help="Classify a single image file and exit (e.g. ~/test.jpg)")
    parser.add_argument("--dry-run-sort", action="store_true",
                        help="In test mode, don't actuate motors—just print the result")
    args = parser.parse_args()

    # sorter = None
    # laser_sensor = None

    try:
        # ---------- Test mode: classify a file WITHOUT initializing the camera ----------
        if args.test_image:
            print(f"[TEST MODE] Classifying file: {args.test_image}")
            # Make classify_image_path a @staticmethod or a separate function that doesn't init the camera
            predicted_labels = CameraManager.classify_image_path(args.test_image)
            best_label = max(predicted_labels, key=predicted_labels.get)
            confidence = predicted_labels[best_label]
            print(f"Predicted: {predicted_labels}")
            waste_type = label_to_waste_type(best_label)
            print(f"WasteType: {waste_type}, Confidence: {confidence}")
            return

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    # ---------- End test mode ----------


if __name__ == "__main__":
    main()

# def main():
#     try:
#         sorter = SortingMechanism(rotation_pin=17, gate_pin=27)
#         identifier = CameraManager()
#         laser_sensor = LaserSensor(laser_pin=23)
#
#         print("Smart Recycling Bin initialized...")
#         print("Waiting for object to enter the bin...")
#
#         while True:
#             while not laser_sensor.is_beam_broken():
#                 time.sleep(0.1)
#
#             print("New item detected!")
#             predicted_label = identifier.capture_image()
#
#             if predicted_label == "Plastic":
#                 waste_type = WasteType.PLASTIC
#             elif predicted_label == "Glass":
#                 waste_type = WasteType.GLASS
#             elif predicted_label == "Metal":
#                 waste_type = WasteType.METAL
#             else:
#                 waste_type = WasteType.OTHER
#
#             print(f"Sorting waste of type: {predicted_label}")
#             sorter.sort_waste(waste_type)
#
#             # Wait until beam is restored before detecting the next object
#             while laser_sensor.is_beam_broken():
#                 time.sleep(0.1)
#
#             print("Item sorted. Waiting for the next item...")
#
#     except KeyboardInterrupt:
#         print("\nProgram interrupted by user")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         traceback.print_exc()
#
#     finally:
#         sorter.cleanup()
#         laser_sensor.cleanup()
#
#
#
#
#
# if __name__ == "__main__":
#     main()
