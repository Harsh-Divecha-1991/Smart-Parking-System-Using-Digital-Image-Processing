import cv2
import pickle

# # load image
# img = cv2.imread('data/img.png')
# width = 156 - 50
# height = 240 - 193
# width, height = 106, 47
# width, height = 400, 300
width, height = 450, 350
# postList = [] 
# try to find the old position list else create empty list
try:
    with open('CarParkPos.pkl', 'rb') as f:
        postList = pickle.load(f)
except:
    postList = [] 


# function's
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        postList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(postList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y+height:
                postList.pop(i)

    # write position list to pickle file 
    with open('CarParkPos.pkl', 'wb') as f:
        pickle.dump(postList, f)

while 1:
    # load image (load image dynamicaly every time like video)
    img_path = 'data/img3.jpg' # 'data/img1.jpg' # 'data/img.png'
    img = cv2.imread(img_path)

    # draw rectrangle
    # cv2.rectangle(img, (50,193), (156,240), (255,0,255), 2)
    for pos in postList:
        cv2.rectangle(img, pos, (pos[0] + width , pos[1] + height), (255,0,255), 2)

    # show image
    cv2.imshow('Image', img)
    # cv2.waitKey(1)

    # detect the mouse click
    cv2.setMouseCallback('Image', mouseClick)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
