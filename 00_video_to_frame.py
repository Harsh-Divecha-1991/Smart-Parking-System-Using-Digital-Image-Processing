import cv2
# import os
# import time
#working

path = r'data\02_Parking_Lot.mov' # r'data\carPark1.MOV' # path1 = 'D:\test1'
vidcap = cv2.VideoCapture(path)

# address = "http://192.168.1.2:8080/video"
# vidcap.open(address)

count = 0

while (vidcap.isOpened()): #success:
  #time.sleep(3)
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imwrite("data/img/frame_%d.jpg" % count, image)
  #cv2.imwrite(os.path.join(path, "straight%d.jpg" % count), image)     # save frame as JPEG file
  #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  #cv2.imwrite(os.path.join(path1, "straightbw%d.jpg" % count), gray)  # save frame as JPEG file
  count += 1