import numpy as np
import cv2
import cvzone
import pickle

# load video
cam = cv2.VideoCapture('data\carPark.mp4')

# width = 156 - 50
# height = 240 - 193
width, height = 106, 47

# load the position list
with open('CarParkPos.pkl', 'rb') as f:
    postList = pickle.load(f)

# functions

# def checkParkingSpace():
#     # # draw rectrangle
#     # # cv2.rectangle(img, (50,193), (156,240), (255,0,255), 2)
#     # for pos in postList:
#     #     cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)

#     for pos in postList:
#         # crop the position one by one
#         x, y = pos
#         imgCrop = img[y:y+height, x:x+width]
#         cv2.imshow(str(x*y), imgCrop)

def checkParkingSpace(imgProcessed):

    spaceCounter = 0

    # # draw rectrangle
    # # cv2.rectangle(img, (50,193), (156,240), (255,0,255), 2)
    # for pos in postList:
    #     cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)

    for pos in postList:
        # crop the position one by one
        x, y = pos
        imgCrop = imgProcessed[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        # cvzone.putTextRect(img, str(count), (x,y+height-3), scale=1, thickness=2, offset=0, colorR=(0,0,255))

        # change color as per the car is present or not
        if (count < 900):
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2
        
        # draw rectrangle
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x,y+height-3), scale=1, thickness=2, offset=0, colorR=color)

    # display the spaceCounter
    cvzone.putTextRect(img, f'Free space are : {spaceCounter} / {len(postList)}', (50, 80), scale=3, thickness=2, offset=0, colorR=(255,0,255))
            
while 1:
    # check the frame count to reset the frame
    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT):
        cam.set(cv2.CAP_PROP_POS_FRAMES,0)

    # read frame from video
    success, img = cam.read()

    # convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # add image blure
    imgBlure = cv2.GaussianBlur(imgGray, (3,3), 1) # play with the parameter here (3,3), 1

    # convert to binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlure, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16) # play with the parameter here (25, 16)
    
    # remove the dot's noice between
    imgMedian = cv2.medianBlur(imgThreshold, 5) # play with the parameter here 5

    # make pixel values more thicker
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) # play with the parameter here 

    # checkParkingSpace()
    checkParkingSpace(imgDilate)

    # # draw rectrangle
    # # cv2.rectangle(img, (50,193), (156,240), (255,0,255), 2)
    # for pos in postList:
    #     cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)
    
    # show image 
    cv2.imshow('Image', img)
    # cv2.imshow('Image Blure', imgBlure)
    # cv2.imshow('Image Threshold', imgThreshold)
    # cv2.imshow('Image Median', imgMedian)
    # cv2.imshow('Image Dilate', imgDilate)
    

    if cv2.waitKey(32) & 0xFF == ord('q'):
        break