import cv2
import numpy as np
#open the main image and convert it to gray scale image
main_image1 = cv2.imread('seg2.jpg')
main_image = cv2.imread('seg2.jpg')
gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
#open the template as gray scale image
template = cv2.imread('trim.jpg', 0)
width, height = template.shape[::-1] #get the width and height
#match the template using cv2.matchTemplate
match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
position = np.where(match >= threshold) #get the location of template in the image
j=0
for point in zip(*position[::-1]): #draw the rectangle around the matched template
   cv2.rectangle(main_image1, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
   j+=1
print(str(j))
cv2.imshow('Template Found', main_image1)
cv2.waitKey(0)
