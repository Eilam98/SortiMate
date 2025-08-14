import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


# api_sec = JF3xzVsAYuFbCBANno6CApSxwck

class DriveUploader:
    def __init__(self, cloud_name="da7yuq42o",
                 api_key="843711719953788",
                 api_secret=""  # copy our API secret
                 ):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )

    def upload_image(self, local_path, label, bin_id, confidence, timestamp):
        file_name = f"{bin_id}_{label}_{confidence}_{timestamp}.jpg"
        if label not in ["Plastic", "Glass", "Paper"]:
            folder_path = f"Home/Other"
        else:
            folder_path = f"Home/{label}"

        result = cloudinary.uploader.upload(local_path, public_id=file_name, folder=folder_path, overwrite=True,
                                            resource_type="image")

        return result["secure_url"]

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# import os
#
#
# class DriveUploader:
#     def __init__(self,
#                  client_secrets_path="/home/pi/creds/client_secrets.json",
#                  creds_path="/home/pi/creds/mycreds.txt",
#                  folder_id = "1GKUtFs8hD5F1LySlFQFir3lY7IUDDKCA"
# ):
#         self.client_secrets_path = client_secrets_path
#         self.creds_path = creds_path
#         self.gauth = None
#         self.drive = None
#         self.folder_id = folder_id
#         self.authenticate()
#
#     def authenticate(self):
#         """Authenticate with Google and create a GoogleDrive client (same flow as your script)."""
#         self.gauth = GoogleAuth()
#         # Needs to be changed based on the location of the client_secrets.json file
#         self.gauth.LoadClientConfigFile(self.client_secrets_path)
#
#         # First time: opens browser for login
#         self.gauth.CommandLineAuth()
#
#         # Save credentials to avoid logging in every time
#         self.gauth.SaveCredentialsFile(self.creds_path)
#
#         self.drive = GoogleDrive(self.gauth)
#         return self.drive
#
#     def upload_image(self, local_path):
#         """Upload a file to the specified Drive folder. Returns the file ID."""
#         if self.drive is None:
#             self.authenticate()
#
#         # Create and upload file
#         file = self.drive.CreateFile({
#             "title": os.path.basename(local_path),
#             "parents": [{"id": self.folder_id}]
#         })
#         file.SetContentFile(local_path)
#         file.Upload()
#
#         # Refresh metadata to get link fields
#         try:
#             file.FetchMetadata(fields="id,webViewLink,webContentLink,alternateLink")
#         except Exception:
#             # older PyDrive sometimes needs a full fetch
#             file.FetchMetadata()
#
#         file_id = file["id"]
#         # Prefer webViewLink when available; otherwise use a standard view URL
#         link = file.get("webViewLink") or file.get("alternateLink") or f"https://drive.google.com/file/d/{file_id}/view"
#
#         print(f"Uploaded: {local_path}")
#         print(f"File ID: {file_id}")
#         print(f"File link: {link}")
#
#         return link
