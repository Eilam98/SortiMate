import cv2
from Classifier import waste_classification

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 'c' to capture an image for classification, or 'ESC' to exit.")

ESC_KEY = 27

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ESC_KEY:
            break
        elif key == ord('c'):
            frame_to_classify = frame.copy()
            predictions = waste_classification(frame_to_classify)
            predicted_label = max(predictions, key=predictions.get)

            print("Predicted waste type: ", predicted_label)
            print("predicted score: ", predictions[predicted_label])

cap.release()
cv2.destroyAllWindows()
