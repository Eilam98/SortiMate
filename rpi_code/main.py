import time
import os
from sorting_mechanism import SortingMechanism, WasteType
from Waste_recognition.CameraManager import CameraManager
from Waste_recognition.Classifier import WasteClassifier
import traceback
from laser_sensor import LaserSensor
from firebase_handler import FirebaseHandler
from monitor_manager import MonitorManager
from push_button import PushButton

# Constants
CLASSIFICATION_THRESHOLD = 0.8
TIME_OUT_USER_ANSWER = 30

# global variables
user_answered = False
user_choice = None


def main():
    try:
        global user_answered, user_choice
        firebase_handler = FirebaseHandler()
        # sorter = SortingMechanism(rotation_pin=17, gate_pin=27)
        camera = CameraManager()
        classifier = WasteClassifier()
        # laser_sensor = LaserSensor(laser_pin=23)
        push_button = PushButton()

        bin_id = load_bin_id()

        monitor = MonitorManager(
            window_size=(1920, 1080),
            display=":0.0",
            monitor_index=1  # Explicitly set to HDMI-2
        )
        monitor.show("default")

        print("Smart Recycling Bin initialized...")
        print("Waiting for object to enter the bin...")

        while True:
            # while not laser_sensor.is_beam_broken():
            #    time.sleep(0.1)
            while not push_button.is_button_pushed():
                time.sleep(0.1)

            monitor.show("classifying")
            print("New item detected!")
            image = camera.capture_image()
            predicted_label, confidence = classifier.waste_classification(image)
            real_predicted_label = predicted_label
            if predicted_label not in ["Plastic", "Glass", "Metal"]:
                predicted_label = "Other"
            print("Predicted waste type:", predicted_label)
            print("Predicted score:", confidence)

            if confidence > CLASSIFICATION_THRESHOLD and predicted_label != "Other":
                if predicted_label == "Plastic":
                    waste_type = WasteType.PLASTIC
                elif predicted_label == "Glass":
                    waste_type = WasteType.GLASS
                elif predicted_label == "Metal":
                    waste_type = WasteType.METAL
            else:
                # TO ADD: monitor for this case
                user_answered = False
                user_choice = None
                waste_type = WasteType.OTHER
                image_cloudinary_link = camera.upload_image_to_cloudinary(bin_id, real_predicted_label, confidence)
                wrong_event_id = firebase_handler.log_wrong_classification(
                    bin_id=bin_id,
                    real_classified_waste_type=real_predicted_label,
                    confidence=confidence,
                    image_cloudinary_url=image_cloudinary_link,
                    user_answered=user_answered
                )

                stop_listener = firebase_handler.listen_for_wrong_classification_answer(
                    wrong_event_id, on_answered=on_answered)

                # Wait (with timeout) for the user's answer
                start_wait = time.time()
                try:
                    while not user_answered and time.time() - start_wait < TIME_OUT_USER_ANSWER:
                        time.sleep(0.1)
                finally:
                    # Make sure we always stop the stream
                    try:
                        stop_listener()
                    except Exception:
                        pass

                # If the user answered in time, override waste_type and update Firebase
                if user_answered:
                    waste_type = WasteType[user_choice.upper()]
                    # Update the wrong_classification document with user's answer
                    try:
                        firebase_handler.update_wrong_classification_user_answer(
                            wrong_event_id, user_choice
                        )
                        print(f"Updated wrong_classification document {wrong_event_id} with user choice: {user_choice}")
                    except Exception as update_err:
                        print(f"Failed to update wrong_classification document: {update_err}")
                else:
                    print("No user answer within timeout; keeping OTHER")
        
            monitor.show(predicted_label)
            # print(f"Sorting waste of type: {predicted_label}")
            # sorter.sort_waste(waste_type)

            monitor.show("summary")
            time.sleep(3)
            monitor.show("default")
            

            try:
                waste_event_id = firebase_handler.log_waste_event(
                    bin_id=bin_id,
                    waste_type=waste_type.name,
                    confidence=confidence
                )
                print(f"Waste event logged with ID: {waste_event_id}")
            except Exception as log_err:
                print(f"Failed to log waste event: {log_err}")

            # Wait until beam is restored before detecting the next object
            # while laser_sensor.is_beam_broken():
            #    time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        print("END")  # TO DELETE
        # sorter.cleanup()
        # laser_sensor.cleanup()
        push_button.cleanup()
        monitor.stop()


def load_bin_id(path="/home/pi/creds/bin_id.txt"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"An error occurred with getting bin ID, Bin ID file not found at {path}")
        traceback.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

# Start a focused listener for THIS item only
def on_answered(doc):
    global user_answered, user_choice
    data = doc.to_dict() or {}
    user_choice = data.get("user_classified_type")
    user_answered = data.get("user_answered")
    print(f"User answered: {user_choice}")


if __name__ == "__main__":
    main()
