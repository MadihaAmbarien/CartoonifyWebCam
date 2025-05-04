import cv2
import numpy as np

def cartoonify(frame):
    # Step 1: Apply bilateral filter to reduce noise while keeping edges sharp
    color = cv2.bilateralFilter(frame, d=9, sigmaColor=250, sigmaSpace=250)

    # Step 2: Convert to grayscale and apply median blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)

    # Step 3: Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blur, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY,
                                   blockSize=9,
                                   C=2)

    # Step 4: Combine color image with edge mask
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access the webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cartoon_frame = cartoonify(frame)
    cv2.imshow('Cartoon Cam', cartoon_frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
