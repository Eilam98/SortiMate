import os
from pathlib import Path
import time
import numpy as np
from PIL import Image
from .Classifier import waste_classification
from picamera2 import Picamera2


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

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])

        # TO DELETE?
        im = Image.fromarray(frame_rgb)
        im.save(os.path.join(self.images_dir, "current_image.jpg"))

        return predicted_label

    def _center_crop(pil_img, frac: float = 0.6):
        """Keep a centered square fraction of the image (e.g., 0.6 = 60% of width/height)."""
        w, h = pil_img.size
        side = int(min(w, h) * frac)
        left = (w - side) // 2
        top = (h - side) // 2
        return pil_img.crop((left, top, left + side, top + side))

    # For testing purposess only
    @staticmethod
    def classify_image_path(path: str) -> str:
        """Classify an image from disk WITHOUT initializing the camera."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Test image not found: {p}")
        pil_img = Image.open(p).convert("RGB")
        return CameraManager._classify_pil(pil_img)

        # ----- SHARED CLASSIFIER BRIDGE -----

    @staticmethod
    def _classify_pil(pil_image: Image.Image) -> str:
        """
        Bridge to your model. `waste_classification` should accept a PIL image
        (or numpy array) and return a label string like 'Plastic'/'Glass'/...
        """
        pil_image = CameraManager._center_crop(pil_image, frac=0.6)
        pil_image = pil_image.resize((224, 224))

        return waste_classification(np.array(pil_image))

    def __del__(self):
        # Stop the camera preview before exiting
        self.picam2.stop_preview()
