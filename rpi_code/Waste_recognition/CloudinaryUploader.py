import cloudinary
import cloudinary.uploader

class CloudinaryUploader:
    def __init__(self, cloud_name="da7yuq42o",
                 api_key="843711719953788",
                 api_secret="JF3xzVsAYuFbCBANno6CApSxwck"  # copy our API secret
                 ):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )

    def upload_image(self, local_path, label, bin_id, confidence, timestamp):
        file_name = f"{bin_id}_{label}_{confidence}_{timestamp}"
        if label in ["Plastic", "Glass", "Paper"]:
            folder_path = label
        else:
            folder_path = "Other"

        result = cloudinary.uploader.upload(local_path, public_id=file_name, folder=folder_path, overwrite=True,
                                            resource_type="image")

        return result["secure_url"]
