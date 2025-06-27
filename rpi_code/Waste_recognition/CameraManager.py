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
            main={"format": "RGB888", "size": (640, 480)} # TO EDIT: size and format
        ))
        self.picam2.start()
        
        #TO DELETE?
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(base_dir, "temporary_images")
        os.makedirs(self.images_dir, exist_ok=True)

    def capture_image(self):
        time.sleep(0.2)  # Let the camera adjust exposure
        frame_bgr = self.picam2.capture_array("main") # Grab the frame – it comes out BGR
        frame_rgb = frame_bgr[..., ::-1] # Convert BGR ➜ RGB (swap channels 0↔2)

        # Run the frame through the waste classifier
        predictions = waste_classification(frame_rgb)
        print("im here after the classifier")
        predicted_label = max(predictions, key=predictions.get)

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])

        # TO DELETE?
        im = Image.fromarray(frame_rgb)
        im.save(os.path.join(self.images_dir, "current_image.jpg"))

        return predicted_label

    def __del__(self):
        # Stop the camera preview before exiting
        self.picam2.stop_preview()
