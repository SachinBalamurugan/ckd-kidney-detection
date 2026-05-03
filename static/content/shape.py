import cv2  
    
# path  
path = 'testing/r23.jpg'
    
# Reading an image in default mode 
image = cv2.imread(path) 
    
# Window name in which image is displayed 
window_name = 'Image'
   
# Center coordinates 
center_coordinates = (390, 240) 
  
# Radius of circle 
radius = 100
   
# Blue color in BGR 
color = (255, 0, 0) 
   
# Line thickness of 2 px 
thickness = 2
   
# Using cv2.circle() method 
# Draw a circle with blue line borders of thickness of 2 px 
image = cv2.circle(image, center_coordinates, radius, color, thickness) 
cv2.imwrite("sample/aaa.jpg",image)
# Displaying the image  
cv2.imshow(window_name, image)  
