from picamera2 import Picamera2
import time
from PIL import Image
from Classifier import waste_classification

image_path = "C://Users//user//Downloads//close_plast.jpg"

# Initialize and configure for still capture
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))

picam2.start()
time.sleep(2)

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
        # Capture the current frame as a NumPy array
        frame = picam2.capture_array()
        print("im here after capture_array")
        # If desired, you can save the image using Pillow:
        im = Image.fromarray(frame)
        im.save('captured.jpg')
        print("im here after save in frame")
        # Run the frame through the waste classifier
        predictions = waste_classification(frame)
        print("im here after the classifier")
        predicted_label = max(predictions, key=predictions.get)

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])
    else:
        print("Invalid command. Please type 'c' or 'q'.")

# Stop the camera preview before exiting
picam2.stop_preview()
