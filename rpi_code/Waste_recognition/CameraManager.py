import os
import time
import numpy as np
from PIL import Image
from .Classifier import waste_classification
from picamera2 import Picamera2
from .DriveUploader import upload_image
import tempfile

FOLDER_ID = "1GKUtFs8hD5F1LySlFQFir3lY7IUDDKCA"


class CameraManager:
    def __init__(self):
        # Initialize and configure for still capture
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(
            main={"format": "RGB888", "size": (640, 480)}  # TO EDIT: size and format
        ))
        self.picam2.start()

        # TO DELETE?
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(base_dir, "temporary_images")
        os.makedirs(self.images_dir, exist_ok=True)

    def capture_image(self):
        time.sleep(0.2)  # Let the camera adjust exposure
        frame_bgr = self.picam2.capture_array("main")  # Grab the frame – it comes out BGR
        frame_rgb = frame_bgr[..., ::-1]  # Convert BGR ➜ RGB (swap channels 0↔2)

        # Run the frame through the waste classifier
        predictions = waste_classification(frame_rgb)
        print("im here after the classifier")
        predicted_label = max(predictions, key=predictions.get)
        confidence = f"{predictions[predicted_label]:.4f}"

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])

        # Save temporarily in memory
        image = Image.fromarray(frame_rgb)
        counter = self.get_and_increment_counter()
        filename = f"{predicted_label}_{counter}_{confidence}.jpg"

        # Use tempfile to store image just for upload
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp_file:
            image.save(tmp_file.name)
            upload_image(tmp_file.name, FOLDER_ID)
            print(f"✅ Uploaded {filename} to Drive (temporary file deleted)")

        # TO DELETE?
        im = Image.fromarray(frame_rgb)
        im.save(os.path.join(self.images_dir, "current_image.jpg"))

        return predicted_label, confidence

    def upload_image_to_drive(self, predicted_label, confidence):

        # Load the image from RPI Camera2's memory
        image_path = os.path.join(self.images_dir, "current_image.jpg")
        image = Image.open(image_path)

        counter = self.get_and_increment_counter()
        filename = f"{predicted_label}_{counter}_{confidence}.jpg"

        # Use tempfile to store image just for upload
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp_file:
            image.save(tmp_file.name)
            upload_image(tmp_file.name, FOLDER_ID)
            print(f"✅ Uploaded {filename} to Drive (temporary file deleted)")

    # Adding counter to make each image unique, and saving it to a file
    def get_and_increment_counter(self):
        counter_file = "image_counter.txt"

        # If file doesn't exist, start at 0
        if not os.path.exists(counter_file):
            with open(counter_file, "w") as f:
                f.write("0")

        # Read current counter
        with open(counter_file, "r") as f:
            counter = int(f.read().strip())

        # Increment and save
        counter += 1
        with open(counter_file, "w") as f:
            f.write(str(counter))

        return counter

    def __del__(self):
        # Stop the camera preview before exiting
        self.picam2.stop_preview()
