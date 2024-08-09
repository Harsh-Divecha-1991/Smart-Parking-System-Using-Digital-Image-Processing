import numpy as np
import cv2
import easyocr
import imutils

reader = easyocr.Reader(['en'])

# capture live video strime
URL = "http://192.168.0.180:8080/video" # "http://192.168.0.91:8080/video"
capture = cv2.VideoCapture(URL)

while 1:

    # read video strime
    _, frame = capture.read()

    # frame.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    # frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
    # frame.set(cv2.CAP_PROP_FPS, 25)

    # Convert colored image into grayscale formate
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Filter and Edge Detection
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) # Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) # Edge detection

    # Find Contours and Apply Mask
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key = cv2.contourArea,reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour,10,True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(frame, frame, mask=mask)

    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    # use easy ocr to read text
    result = reader.readtext(cropped_image)
    print(f"Number Plate : {result}")


    # Render Result

    text = result[0][-2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(frame, 
                    text=text, 
                    org=(approx[0][0][0]-25, approx[1][0][1]-20), 
                    fontFace=font, 
                    fontScale=1, 
                    color=(0,255,0), 
                    thickness=2, 
                    lineType=cv2.LINE_AA)
    res = cv2.rectangle(frame, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0), 3)

    # show the video strime
    # cv2.imshow('LiveStrimeScreen', frame)
    cv2.imshow('LiveStrimeScreen1', res)


    # to stop the strime
    if cv2.waitKey(1) == ord("q"):
        break

# close the resorces
capture.release()
cv2.destroyAllWindows()