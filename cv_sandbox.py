import cv2 as cv
img = cv.imread("assets/prog_drawing.png")

cv.imshow("Display window", img)
k = cv.waitKey(0) # Wait for a keystroke in the window
