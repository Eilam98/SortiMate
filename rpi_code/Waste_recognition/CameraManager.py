import os
import time
from PIL import Image
from picamera2 import Picamera2
from Waste_recognition import DriveUploader
import tempfile


class CameraManager:
    def __init__(self):
        # Initialize and configure for still capture
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration(
            main={"format": "RGB888", "size": (3280, 2464)}
        ))
        self.picam2.set_controls({"ScalerCrop": (820, 616, 1640, 1232)})
        self.picam2.start()

        self.drive_manager = DriveUploader.DriveUploader()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(base_dir, "temporary_images")
        os.makedirs(self.images_dir, exist_ok=True)

    def capture_image(self):
        time.sleep(0.2)
        frame_bgr = self.picam2.capture_array("main")
        frame_rgb = frame_bgr[..., ::-1]

        im = Image.fromarray(frame_rgb)
        im.save(os.path.join(self.images_dir, "current_image.jpg"))

        return frame_rgb

    def upload_image_to_drive(self, bin_id, predicted_label, confidence, timestamp=time.time()):
        image_path = os.path.join(self.images_dir, "current_image.jpg")
        if not os.path.exists(image_path):
            print("No image found to upload.")
            return None

        image = Image.open(image_path)
        filename = f"{bin_id}_{predicted_label}_{confidence}_{timestamp}.jpg"

        # Use a temporary file for upload
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp_file:
            image.save(tmp_file.name)
            image_url = self.drive_manager.upload_image(
                local_path=tmp_file.name,
                label=predicted_label,
                bin_id=bin_id,
                confidence=confidence,
                timestamp=timestamp
            )

            print(f"Uploaded {filename} to Cloudinary")

        return image_url

    # def upload_image_to_drive(self, bin_id, predicted_label, confidence, timestamp=time.time()):
    #     # Load the image from RPI Camera2's memory
    #     image_path = os.path.join(self.images_dir, "current_image.jpg")
    #     if not os.path.exists(image_path):
    #         print("No image found to upload.")
    #         return
    #
    #     image = Image.open(image_path)
    #     filename = f"{bin_id}_{predicted_label}_{confidence}_{timestamp}.jpg"
    #
    #     # Use tempfile to store image just for upload
    #     with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp_file:
    #         image.save(tmp_file.name)
    #         image_drive_link = self.drive_manager.upload_image(tmp_file.name)
    #         print(f"Uploaded {filename} to Google Drive")
    #
    #     return image_drive_link

    def __del__(self):
        # Stop the camera preview before exiting
        self.picam2.stop_preview()
