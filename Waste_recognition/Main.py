import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained waste classification model.
# Ensure that the model is trained to accept images of the size you pre-process to (e.g., 224x224 pixels).
model = tf.keras.models.load_model('waste_classifier.h5')


def capture_image():
    """Capture an image from the webcam and return it."""
    cap = cv2.VideoCapture(0)  # Use device 0 for the default camera
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Failed to capture image from camera.")
    # Optionally, save the captured image to disk for verification
    cv2.imwrite("captured_image.jpg", frame)
    return frame


def preprocess_image(image):
    """
    Preprocess the captured image to match the model input.
    Resize the image to 224x224 pixels (adjust if your model requires a different size),
    normalize the pixel values, and expand dimensions for batch processing.
    """
    resized = cv2.resize(image, (224, 224))
    normalized = resized.astype("float32") / 255.0
    # Expand dimensions to create a batch of size 1
    preprocessed = np.expand_dims(normalized, axis=0)
    return preprocessed


def classify_image(image, model):
    """Use the model to predict the waste category from the preprocessed image."""
    preds = model.predict(image)
    # The predicted class is the one with the highest probability
    class_idx = np.argmax(preds, axis=1)[0]
    # Map the index to a human-readable label
    classes = ["plastic bottles", "glass bottles", "aluminum cans", "others"]
    return classes[class_idx]


def main():
    try:
        # Step 1: Capture an image from the camera
        image = capture_image()
        # Step 2: Preprocess the image to match the model's input format
        processed_image = preprocess_image(image)
        # Step 3: Classify the image using the model
        category = classify_image(processed_image, model)
        print("Predicted waste category:", category)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
