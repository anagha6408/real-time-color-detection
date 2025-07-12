import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)

# Dummy function for trackbars
def nothing(x):
    pass

# Create window and trackbars
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

# Define a simple function to identify color from HSV value
def get_color_name(h, s, v):
    if v < 50:
        return "Black"
    elif s < 50 and v > 200:
        return "White"
    elif s < 50:
        return "Gray"
    elif h < 10 or h > 160:
        return "Red"
    elif 10 < h <= 25:
        return "Orange"
    elif 25 < h <= 35:
        return "Yellow"
    elif 35 < h <= 85:
        return "Green"
    elif 85 < h <= 125:
        return "Blue"
    elif 125 < h <= 160:
        return "Purple"
    else:
        return "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally (mirror effect)
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbar positions
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Get center pixel's HSV value
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    center_hsv = hsv[center_y, center_x]
    h, s, v = center_hsv
    color_name = get_color_name(h, s, v)

    # Draw a small circle at center
    cv2.circle(frame, (center_x, center_y), 5, (255, 255, 255), -1)

    # Put color name on the frame
   # Convert the HSV value to BGR to use as text color
    bgr_color = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
    bgr_color = tuple(int(c) for c in bgr_color)  # Convert to int tuple

    # Put color name text on the frame using the detected color
    cv2.putText(frame, f"Color: {color_name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, bgr_color, 2)

    # Show the frames
    cv2.imshow("Original Frame", frame)
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Color Detected", result)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
