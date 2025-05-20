import subprocess
import time
import os
from pathlib import Path
import numpy as np
from PIL import Image
from Classifier import waste_classification


class CameraManager:
    
    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        out_dir: str = "temporary_images",
        filename: str = "current_image.jpg",
    ):
        self.width = width
        self.height = height
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(exist_ok=True)
        self.img_path = self.out_dir / filename

    def identify_item(self) -> str:
        """
        Uses `libcamera-jpeg` to grab a frame, then calls
        `waste_classification(frame_array)`.

        Returns
        -------
        str
            The predicted class label (highest-scoring key).
        """
        self._capture_frame()
        frame = self._load_frame_as_array()

        # TO EDIT: change design
        predictions = waste_classification(frame)
        predicted_label = max(predictions, key=predictions.get)

        print("Predicted waste type:", predicted_label)
        print("Predicted score:", predictions[predicted_label])

        return predicted_label

    def _capture_frame(self) -> None:
        """
        Calls libcamera-jpeg once.  The '-n' flag suppresses preview.
        """
        cmd = [
            "libcamera-jpeg",
            "-n",                      # no preview window
            "--width",  str(self.width),
            "--height", str(self.height),
            "-o",       str(self.img_path),
        ]
        subprocess.run(cmd, check=True)  # raises if capture fails

    def _load_frame_as_array(self) -> np.ndarray:
        """
        Loads the captured JPEG -> RGB NumPy array suitable for our model.
        """
        img = Image.open(self.img_path).convert("RGB")
        return np.asarray(img)