import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ESC_KEY = 27
while True:
    success, frame = cap.read()
    if success:
        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ESC_KEY:  # esc button is being pressed to quit filming
            break

cv2.destroyAllWindows()
