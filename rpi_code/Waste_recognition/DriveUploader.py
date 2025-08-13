from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class DriveUploader:
    def __init__(self,
                 client_secrets_path="/home/pi/creds/client_secrets.json",
                 creds_path="/home/pi/creds/mycreds.txt",
                 folder_id = "1GKUtFs8hD5F1LySlFQFir3lY7IUDDKCA"
):
        self.client_secrets_path = client_secrets_path
        self.creds_path = creds_path
        self.gauth = None
        self.drive = None
        self.folder_id = folder_id
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google and create a GoogleDrive client (same flow as your script)."""
        self.gauth = GoogleAuth()
        # Needs to be changed based on the location of the client_secrets.json file
        self.gauth.LoadClientConfigFile(self.client_secrets_path)

        # First time: opens browser for login
        self.gauth.LocalWebserverAuth()

        # Save credentials to avoid logging in every time
        self.gauth.SaveCredentialsFile(self.creds_path)

        self.drive = GoogleDrive(self.gauth)
        return self.drive

    def upload_image(self, local_path):
        """Upload a file to the specified Drive folder. Returns the file ID."""
        if self.drive is None:
            self.authenticate()

        # Create and upload file
        file = self.drive.CreateFile({
            "title": os.path.basename(local_path),
            "parents": [{"id": self.folder_id}]
        })
        file.SetContentFile(local_path)
        file.Upload()

        print(f"Uploaded: {local_path}")
        print(f"File link: https://drive.google.com/file/d/{file['id']}/view")
        return file["id"]