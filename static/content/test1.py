import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os

import cv2

from PIL import Image, ImageOps
import scipy.ndimage as ndi

sdir=os.listdir('content/data/')
#print(sdir)


sdir2=os.listdir('content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/')
#print(sdir2)

path_main = 'content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/'
for folder in os.listdir(path_main):
    list_of_elements = os.listdir(os.path.join(path_main, folder)) 
    print(f'Folder: {folder}\n')
    print(f'Number of elements: {len(list_of_elements)}\n')
    #print(f'First item\'s name: {list_of_elements[0]}\n')
    print('***************************')

def plot_imgs(item_dir, num_imgs=25):
    all_item_dirs = os.listdir(item_dir)
    item_files = [os.path.join(item_dir, file) for file in all_item_dirs][:num_imgs]
    #print("path")
    #print(item_files)
    plt.figure(figsize=(10, 10))
    for idx, img_path in enumerate(item_files):
        plt.subplot(5, 5, idx+1)
        img = plt.imread(img_path)
        plt.title(f'{img_path}'[-10:-4])
        plt.imshow(img)

    #plt.show()
    plt.tight_layout()
    plt.close()
##########
path_normal = 'content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Normal/'
path_stone = 'content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Stone/'
path_cyst = 'content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Cyst/'
path_tumor = 'content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Tumor/'

plot_imgs(path_normal, 5)
plot_imgs(path_stone, 5)
plot_imgs(path_cyst, 5)
plot_imgs(path_tumor, 5)

data_kidney_path = 'content/data/kidneyData.csv'
dd=df_kidney = pd.read_csv(data_kidney_path, header=0)
#print(dd)
df_kidney.head()
df_kidney.tail()
df_kidney.info()
df_kidney['Class'].unique()
kidney_classes = df_kidney['Class'].value_counts()
sum_of_element = kidney_classes.sum()
plot_bar = kidney_classes.plot.bar(title='Total number of items in classes')
plot_bar.bar_label(plot_bar.containers[0])
#plt.show()
plt.close()
##############################

def size_imgs(item_dir, num_imgs=5):
    all_item_dirs = os.listdir(item_dir)
    if num_imgs == -1:
        item_files = [os.path.join(item_dir, file) for file in all_item_dirs]
    else:
        item_files = [os.path.join(item_dir, file) for file in all_item_dirs][:num_imgs]
    img_shape_list = []
    number_sizes = {}
    
    for idx, img_path in enumerate(item_files):
        img = plt.imread(img_path)
        img_shape_list.append(img.shape)
        
    unique = list(set(img_shape_list))
    
    for item in unique:
        number_sizes[item] = img_shape_list.count(item)
    
    return number_sizes
#############
imgs_sizes_dict_normal = size_imgs(path_normal, num_imgs=-1)

elements_string_normal = list(map(str, imgs_sizes_dict_normal.keys()))

plt.figure(figsize=(5, 10))
plt.barh(elements_string_normal, imgs_sizes_dict_normal.values());
plt.title('Shapes of images in Normal folder');
#plt.show()
plt.close()
###########################
imgs_sizes_dict_cyst = size_imgs(path_cyst, num_imgs=-1)

elements_string_cyst = list(map(str, imgs_sizes_dict_cyst.keys()))

plt.figure(figsize=(5, 10))
plt.barh(elements_string_cyst, imgs_sizes_dict_cyst.values());
plt.title('Shapes of images in Cyst folder');
#plt.show()
plt.close()
########################
imgs_sizes_dict_tumor = size_imgs(path_tumor, num_imgs=-1)

elements_string_tumor = list(map(str, imgs_sizes_dict_tumor.keys()))

plt.figure(figsize=(5, 10))
plt.barh(elements_string_tumor, imgs_sizes_dict_tumor.values());
plt.title('Shapes of images in Tumor folder');
#plt.show()
plt.close()
#########################
imgs_sizes_dict_stone = size_imgs(path_stone, num_imgs=-1)

elements_string_stone = list(map(str, imgs_sizes_dict_stone.keys()))

plt.figure(figsize=(5, 10))
plt.barh(elements_string_stone, imgs_sizes_dict_stone.values());
plt.title('Shapes of images in Stone folder');
#plt.show()
plt.close()
#############################
img_sizes_total = {**imgs_sizes_dict_normal, **imgs_sizes_dict_stone, **imgs_sizes_dict_tumor, **imgs_sizes_dict_cyst}

elements_string_total = list(map(str, img_sizes_total.keys()))

plt.figure(figsize=(10, 18))
plt.barh(elements_string_total, img_sizes_total.values());
plt.title('Shapes of all images');
#plt.show()
plt.close()

####################################

img_sizes_total[(512, 512, 3)]
print(f'{round(img_sizes_total[(512, 512, 3)]/sum_of_element,4)*100}%')

plt.figure(figsize=(15, 15))
plt.pie(img_sizes_total.values(), labels=elements_string_total);
plt.title('Shapes of all images');
plt.show()
plt.close()

##########################

print('Normal')
for element in [(512, 512, 3)]:
    if element in imgs_sizes_dict_normal.keys():
        print(f'{element}\n')
print('*******************\n')
print('Cyst\n')
for element in [(512, 512, 3)]:
    if element in imgs_sizes_dict_cyst.keys():
        print(f'{element}\n')
print('*******************\n')
print('Tumor\n') 
for element in [(512, 512, 3)]:
    if element in imgs_sizes_dict_tumor.keys():
        print(f'{element}\n')
print('*******************\n')
print('Stone\n')   
for element in [(512, 512, 3)]:
    if element in imgs_sizes_dict_stone.keys():
        print(f'{element}\n')

###
list_bigger_than_first_512_img = [val for val in list(map(tuple, img_sizes_total.keys())) if val[0] < 512]
list_bigger_than_first_512_img

print(f"Total number of images in dataset: {sum_of_element}")
print(f"Total number of different shapes of images in dataset: {len(img_sizes_total)}")
for element in list_bigger_than_first_512_img:
    print(f'Shape: {element} - number of elements: {img_sizes_total[element]} - percentage of the dataset: {round(img_sizes_total[element]/sum_of_element,4)*100}%')


list_bigger_than_second_512_img = [val for val in list(map(tuple, img_sizes_total.keys())) if val[1] < 512]
list_bigger_than_second_512_img

####

print('Normal')
for element in [(504, 622, 3), (476, 588, 3), (451, 559, 3)]:
    if element in imgs_sizes_dict_normal.keys():
        print(f'{element}\n')
print('*******************\n')
print('Cyst\n')
for element in [(504, 622, 3), (476, 588, 3), (451, 559, 3)]:
    if element in imgs_sizes_dict_cyst.keys():
        print(f'{element}\n')
print('*******************\n')
print('Tumor\n') 
for element in [(504, 622, 3), (476, 588, 3), (451, 559, 3)]:
    if element in imgs_sizes_dict_tumor.keys():
        print(f'{element}\n')
print('*******************\n')
print('Stone\n')   
for element in [(504, 622, 3), (476, 588, 3), (451, 559, 3)]:
    if element in imgs_sizes_dict_stone.keys():
        print(f'{element}\n')

###

        




