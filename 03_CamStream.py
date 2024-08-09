import cv2

# capture live video strime
URL = "http://192.168.0.91:8080/video"
capture = cv2.VideoCapture(URL)

while 1:

    # read video strime
    _, frame = capture.read()

    # show the video strime
    cv2.imshow('LiveStrimeScreen', frame)


    # to stop the strime
    if cv2.waitKey(1) == ord("q"):
        break

# close the resorces
capture.release()
cv2.destroyAllWindows()