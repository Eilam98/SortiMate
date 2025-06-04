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

        print("Type 'c' (then press Enter) to capture an image for classification.")
        print("Type 'q' (then Enter) to exit the program.")

        bin_id = "bin_001"
        user_id = "default_user"  # Replace with actual user_id logic if available
        while True:
            # laser_sensor.wait_for_beam_break()

            start_time = time.time()
            try:
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

                # Log waste event
                log_waste_event(
                    bin_id=bin_id,
                    waste_type=waste_type.name,  # Use enum name as string
                    user_id=user_id,
                    latency_ms=latency_ms,
                    confidence=confidence
                )

                # Update bin status (add more fields as needed)
                update_bin_status(
                    bin_id=bin_id
                )

                # Create alert if needed (example: low confidence)
                if confidence is not None and confidence < 0.5:
                    create_alert(
                        bin_id=bin_id,
                        message=f"Low confidence in waste classification: {predicted_label} ({confidence:.2f})",
                        alert_type="low_confidence"
                    )

            except Exception as e:
                print(f"Error during waste processing: {e}")
                log_waste_event(
                    bin_id=bin_id,
                    waste_type="UNKNOWN",
                    user_id=user_id,
                    is_error=True,
                    error_message=str(e)
                )
                create_alert(
                    bin_id=bin_id,
                    message=f"Error: {str(e)}",
                    alert_type="system_error"
                )

            # Wait until beam is restored before detecting the next object
            #while laser_sensor.is_beam_broken():
            #    time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        sorter.cleanup()
     #   laser_sensor.cleanup()

if __name__ == "__main__":
    main()
