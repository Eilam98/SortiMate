import os
from pathlib import Path
import numpy as np
from PIL import Image
from .Classifier import waste_classification
from picamera2 import Picamera2

class CameraManager:
    def __init__(self):
        # Initialize and configure for still capture
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(
            main={"format": "RGB888", "size": self.picam2.sensor_resolution} # TO EDIT: size and format
        ))
        self.picam2.start()
        
        #TO DELETE?
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(base_dir, "temporary_images")
        os.makedirs(images_dir, exist_ok=True)

    def capture_image(self):
        # Capture the current frame as a NumPy array
        frame = self.picam2.capture_array()
        print("im here after capture_array")
        # If desired, you can save the image using Pillow:
        print("im here after save in frame")
        # Run the frame through the waste classifier
        predictions = waste_classification(frame)
        print("im here after the classifier")
        predicted_label = max(predictions, key=predictions.get)

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])

        # TO DELETE?
        im = Image.fromarray(frame)
        im.save(os.path.join(temp_dir, "current_image.jpg"))

        return predicted_label

    def __del__(self):
        # Stop the camera preview before exiting
        self.picam2.stop_preview()
