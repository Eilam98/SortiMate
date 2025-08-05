from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


# Authenticate and create PyDrive client
def authenticate_drive():
    gauth = GoogleAuth()

    gauth.LoadClientConfigFile("C:/Users/user/Desktop/Project_SortiMate/SortiMate/rpi_code/Waste_recognition/client_secrets.json")

    # First time: opens browser for login
    gauth.LocalWebserverAuth()

    # Save credentials to avoid logging in every time
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    return drive


# Upload file to a specific folder
def upload_image(local_path, drive_folder_id):
    drive = authenticate_drive()

    # Create and upload file
    file = drive.CreateFile({
        "title": os.path.basename(local_path),
        "parents": [{"id": drive_folder_id}]
    })
    file.SetContentFile(local_path)
    file.Upload()

    print(f"✅ Uploaded: {local_path}")
    print(f"🌐 File link: https://drive.google.com/file/d/{file['id']}/view")


# Example usage
if __name__ == "__main__":
    # Replace this with your real folder ID from Google Drive
    folder_id = "1GKUtFs8hD5F1LySlFQFir3lY7IUDDKCA"

    # Example image path to upload
    image_path = "C:/Users/user/Downloads/4804-0001.jpg"

    upload_image(image_path, folder_id)
