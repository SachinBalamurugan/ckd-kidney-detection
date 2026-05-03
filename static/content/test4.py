import pydicom
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import PIL
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import cv2
from skimage import measure
import scipy
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
from scipy.ndimage import zoom
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px

def load_scan(path):
    slices = [pydicom.read_file(path+"/"+s) for s in os.listdir(path) ]
    slices.sort(key = lambda x: int(x.AcquisitionNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        s.SamplesPerPixel = 1
        
    return slices

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans[:100]])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)
    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)
def make_mesh(image,threshold=100):
    print( "Transposing surface")
    p = image.transpose(2,1,0)
    print( "Calculating surface")
    verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold) 
    return verts, faces

def plotly_3d(verts, faces):
    x,y,z = zip(*verts)   
    print("Drawing")
    # Make the colormap single color since the axes are positional not intensity. 
    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
    #colormap = ['rgb(100,149,237)','rgb(100,149,237)']
    #mesh.set_facecolor(face_color)
    fig = FF.create_trisurf(x=x,
                        y=y, 
                        z=z, 
                        plot_edges=False,
                        colormap=colormap,
                        simplices=faces,
                        backgroundcolor='rgb(64, 64, 64)',
                        title="Interactive Visualization")
    iplot(fig)
def get_y(df):
    dic = {True:1,False:0}
    df['Contrast'] = df['Contrast'].map(dic)
    y =df['Contrast'].values
    return y

path =  "dicom_dir/"
#id=0
patient = load_scan(path)
imgs = get_pixels_hu(patient)


fig = plt.figure(figsize=(20,20))
for num,image in enumerate(imgs[:12]):
    ax = fig.add_subplot(3,4,num+1)
    ax.imshow(image, cmap=plt.cm.bone)
    ax.set_title(f"The age of this patient:{patient[num].PatientAge}\nAnd is a {patient[num].PatientSex}")
plt.show()



img = np.copy(imgs[0])
fig = px.histogram(x=img.flatten())
fig.show()


seg1 = (img<-2000)
seg2 = (img>-2000) & (img<-1000)
seg3 = (img>-1000) & (img<-500)
seg4 = (img>-500)
all_seg = np.zeros((img.shape[0],img.shape[1],3))
all_seg[seg1] = (1,0,0)
all_seg[seg2] = (0,1,0)
all_seg[seg3] = (0,0,1)
all_seg[seg4] = (1,1,0)
#plt.imshow(all_seg)
#plt.show()
fig = px.imshow(all_seg)
fig.show()





