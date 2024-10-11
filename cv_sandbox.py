import cv2 as cv
import numpy as np

def display_image():
    img = cv.imread("assets/prog_drawing.png")
    cv.imshow("Display window", img)
    k = cv.waitKey(0)

def disp_real_time_video():
    cap = cv.VideoCapture(2)

    if not cap.isOpened():
        print("Error could not open webcam")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print('Error failed to capture frame')
            break

        cv.imshow("Camera", frame)
        # Press 'q' to quit the video window
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        if cv.waitKey(1) & 0xFF == ord('1'):
            cap = cv.VideoCapture(1)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cap = cv.VideoCapture(2)


    cap.release()
    cv.destroyAllWindows()

disp_real_time_video()