import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

def main():
    real_prdicted_label = "Plastic"
    # Configuration
    cloudinary.config(
        cloud_name = "da7yuq42o",
        api_key = "843711719953788",
        api_secret = "", # Click 'View API Keys' above to copy your API secret
        secure=True
    )
    if real_prdicted_label == "Plastic":

        upload_result = cloudinary.uploader.upload("C:/Users/user/Downloads/plastic8.jpg",
                                               folder="Plastic")
    print(upload_result["secure_url"])

    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
    print(optimize_url)

    # Transform the image: auto-crop to square aspect_ratio
    auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
    print(auto_crop_url)

if __name__ == '__main__':
    main()