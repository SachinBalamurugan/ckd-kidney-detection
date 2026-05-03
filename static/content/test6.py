import cv2
import numpy as np
import PIL.Image
from PIL import Image, ImageChops
###fg
'''img = cv2.imread('Tumor- (1007).jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
segment = cv2.subtract(sure_bg,sure_fg)
img = Image.fromarray(img)
segment = Image.fromarray(segment)
path3="seg1.jpg"
segment.save(path3)
###################################################################################
img = cv2.imread('seg1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
segment = cv2.subtract(sure_bg,sure_fg)
img = Image.fromarray(img)
segment = Image.fromarray(segment)
path3="seg2.jpg"
segment.save(path3)'''
########################################################
#open the main image and convert it to gray scale image
main_image1 = cv2.imread('dataset/train/Cyst/c1.jpg')


main_image = cv2.imread('content/bg/x1.jpg')

gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
#open the template as gray scale image
template = cv2.imread('dataset/mask/m2.jpg', 0)
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
if j>0:
    cv2.imshow('Template Found', main_image1)
    cv2.waitKey(0)
      
