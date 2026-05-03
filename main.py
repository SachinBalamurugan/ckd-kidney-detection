# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse

import urllib.request
import urllib.parse   
import csv

# necessary imports 
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import splitfolders
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import seaborn as sns
import splitfolders
#pip install split-folders
'''from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import seaborn as sns
import keras as k
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam'''
##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="ckd_kidney"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    return render_template('index.html',msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg)

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO register(id,name,email,uname,pass) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid,name,email,uname,pass1)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('login_user'))
    return render_template('register.html',msg=msg)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    msg=""
    data=[]
    act=request.args.get("act")

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':

        level=request.form['level'] 
        details=request.form['details']        

        mycursor.execute("SELECT max(id)+1 FROM suggestion")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO suggestion(id,level,details) VALUES (%s, %s, %s)"
        val = (maxid,level,details)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('add_data'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from suggestion where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_data'))

    mycursor.execute('SELECT * FROM suggestion')
    data = mycursor.fetchall()
        
    return render_template('add_data.html',msg=msg,data=data)

@app.route('/add_hos', methods=['GET', 'POST'])
def add_hos():
    msg=""
    data=[]
    act=request.args.get("act")

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':

        doctor=request.form['doctor'] 
        address=request.form['address']
        contact=request.form['contact']   

        mycursor.execute("SELECT max(id)+1 FROM hospital")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO hospital(id,doctor,address,contact) VALUES (%s, %s, %s, %s)"
        val = (maxid,doctor,address,contact)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('add_hos'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from hospital where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_hos'))

    mycursor.execute('SELECT * FROM hospital')
    data = mycursor.fetchall()
        
    return render_template('add_hos.html',msg=msg,data=data)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""

    x = os.listdir("./dataset")
    #print(x)
    
    if request.method=='POST':
        ckd=request.form['ckd']
        if ckd=="1":
            return redirect(url_for('process1',act='1'))
        else:
            return redirect(url_for('img_process1',act='1'))
        
    return render_template('admin.html',msg=msg,dfile=x)

@app.route('/img_process1', methods=['GET', 'POST'])
def img_process1():
    

    return render_template('img_process1.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        #img = cv2.imread('static/dataset/data/'+fname)
        #rez = cv2.resize(img, (300, 300))
        #cv2.imwrite("static/dataset/data1/"+fname, rez)

        
        ##noice
        #img = cv2.imread('static/dataset/'+fname) 
        #dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        #fname2='ns_'+fname
        #cv2.imwrite("static/upload/"+fname2, dst)

    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
        ##bin
        image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        #cv2.imwrite("static/upload/bin_"+fname, thresh)
        

        ###fg
        img = cv2.imread('static/dataset/'+fname)
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
        path3="static/upload/fg_"+fname
        #segment.save(path3)
        ####
        img = cv2.imread('static/upload/fg_'+fname)
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
        path3="static/upload/fg_"+fname
        #segment.save(path3)


    return render_template('pro2.html',dimg=dimg)


@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    i=1
    while i<=50:
        fname="r"+str(i)+".jpg"
        dimg.append(fname)

        img = Image.open('static/data/classify/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        i+=1
    i=1
    j=51
    while i<=10:
        
        fname="r"+str(j)+".jpg"
        dimg.append(fname)

        img = Image.open('static/dataset/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        j+=1
        i+=1

        

    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro4.html',dimg=dimg)

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    i=1
    while i<=60:
        fname="ff_r"+str(i)+".jpg"
        dimg.append(fname)
        i+=1

    return render_template('pro5.html',dimg=dimg)

@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/data/classify'
    ff=open("static/upload/extract.txt",'r')
    ext=ff.read()
    ff.close()
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    feature=ext.split('|')
    class1=feature[0].split(',')
    class2=feature[1].split(',')
    class3=feature[2].split(',')
    class4=feature[3].split(',')
    for cla1 in class1:
        fname='r'+cla1+'.jpg'
        data1.append(fname)
    for cla2 in class2:
        fname='r'+cla2+'.jpg'
        data2.append(fname)
    for cla3 in class3:
        fname='r'+cla3+'.jpg'
        data3.append(fname)
    for cla4 in class4:
        fname='r'+cla4+'.jpg'
        data4.append(fname)


    #######
    sdir=os.listdir('static/content/data/')
    #print(sdir)


    sdir2=os.listdir('static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/')
    #print(sdir2)

    path_main = 'static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/'
    for folder in os.listdir(path_main):
        list_of_elements = os.listdir(os.path.join(path_main, folder)) 
        #print(f'Folder: {folder}\n')
        #print(f'Number of elements: {len(list_of_elements)}\n')
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
    #path_normal = 'static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Normal/'
    #path_stone = 'static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Stone/'
    #path_cyst = 'static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Cyst/'
    #path_tumor = 'static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/Tumor/'

    path_normal = 'static/data/train/Normal/'
    path_stone = 'static/data/train/Stone/'
    path_cyst = 'static/data/train/Cyst/'
    path_tumor = 'static/data/train/Tumor/'

    #plot_imgs(path_normal, 5)
    #plot_imgs(path_stone, 5)
    #plot_imgs(path_cyst, 5)
    #plot_imgs(path_tumor, 5)

    data_kidney_path = 'static/content/data/kidneyData.csv'
    df_kidney = pd.read_csv(data_kidney_path, header=0)
    df_kidney.head()
    df_kidney.tail()
    #df_kidney.info()
    df_kidney['Class'].unique()
    kidney_classes = df_kidney['Class'].value_counts()
    sum_of_element = kidney_classes.sum()

    #########################

    '''plot_bar = kidney_classes.plot.bar(title='Predicted Classes')
    plot_bar.bar_label(plot_bar.containers[0])
    plt.xticks(rotation=0)
    #plt.show()
    plt.savefig("static/upload/gr_kidney_class.jpg")
    plt.close()'''

    #####
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

    '''plt.figure(figsize=(5, 10))
    plt.barh(elements_string_normal, imgs_sizes_dict_normal.values());
    plt.title('Shapes of images in Normal folder');
    plt.savefig("static/upload/gr_shape1.jpg")
    #plt.show()
    plt.close()'''
    ###########################
    imgs_sizes_dict_cyst = size_imgs(path_cyst, num_imgs=-1)

    elements_string_cyst = list(map(str, imgs_sizes_dict_cyst.keys()))

    '''plt.figure(figsize=(5, 10))
    plt.barh(elements_string_cyst, imgs_sizes_dict_cyst.values());
    plt.title('Shapes of images in Cyst folder');
    plt.savefig("static/upload/gr_shape2.jpg")
    #plt.show()
    plt.close()'''
    ########################
    imgs_sizes_dict_tumor = size_imgs(path_tumor, num_imgs=-1)

    elements_string_tumor = list(map(str, imgs_sizes_dict_tumor.keys()))

    '''plt.figure(figsize=(5, 10))
    plt.barh(elements_string_tumor, imgs_sizes_dict_tumor.values());
    plt.title('Shapes of images in Tumor folder');
    plt.savefig("static/upload/gr_shape3.jpg")
    #plt.show()
    plt.close()'''
    #########################
    imgs_sizes_dict_stone = size_imgs(path_stone, num_imgs=-1)

    elements_string_stone = list(map(str, imgs_sizes_dict_stone.keys()))

    '''plt.figure(figsize=(5, 10))
    plt.barh(elements_string_stone, imgs_sizes_dict_stone.values());
    plt.title('Shapes of images in Stone folder');
    #plt.show()
    plt.savefig("static/upload/gr_shape4.jpg")
    plt.close()'''
    #############################
    img_sizes_total = {**imgs_sizes_dict_normal, **imgs_sizes_dict_stone, **imgs_sizes_dict_tumor, **imgs_sizes_dict_cyst}

    elements_string_total = list(map(str, img_sizes_total.keys()))

    '''plt.figure(figsize=(10, 18))
    plt.barh(elements_string_total, img_sizes_total.values());
    plt.title('Shapes of all images');
    #plt.show()
    plt.savefig("static/upload/gr_shape.jpg")
    plt.close()'''

    ####################################

    img_sizes_total[(512, 512, 3)]
    print(f'{round(img_sizes_total[(512, 512, 3)]/sum_of_element,4)*100}%')

    '''plt.figure(figsize=(15, 15))
    plt.pie(img_sizes_total.values(), labels=elements_string_total);
    plt.title('Shapes of all images');
    #plt.show()
    plt.savefig("static/upload/gr_shapeall.jpg")
    plt.close()'''

    

    ###############################
    '''splitfolders.ratio(
        "static/content/data/CT KIDNEY DATASET Normal, CYST, TUMOR and STONE/",
       output="static/data",
       seed=7,
       ratio=(0.90,0.050, 0.050)
    )
    train_datagen = ImageDataGenerator(rescale=1/255)
    valid_datagen = ImageDataGenerator(rescale=1/255)
    test_datagen = ImageDataGenerator(rescale=1/255)

    

    train_dataset = train_datagen.flow_from_directory('./static/data/train',
                                                      target_size=(200, 200),
                                                      color_mode='grayscale', 
                                                      class_mode='categorical', 
                                                      batch_size=100,
                                                      )

    test_dataset = test_datagen.flow_from_directory('./static/data/test',
                                                    target_size=(200, 200),
                                                    class_mode='categorical',
                                                    color_mode='grayscale',
                                                    batch_size=100,
                                                    shuffle=False
                                                    )

    valid_dataset = valid_datagen.flow_from_directory('./static/data/val',
                                                      target_size=(200, 200),
                                                      class_mode='categorical',
                                                      batch_size=100,
                                                      color_mode='grayscale',
                                                      )


    ##################################
    model = Sequential()

    model.add(Conv2D(32, (3,3), activation='relu', input_shape=train_dataset.image_shape))
    model.add(MaxPool2D(2))

    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPool2D(2))


    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(2))

    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(2))


    model.add(Conv2D(128, (3,3), activation='relu'))
    model.add(MaxPool2D(2))

    model.add(Conv2D(128, (3,3), activation='relu'))
    model.add(MaxPool2D(2))


    model.add(Flatten())

    model.add(Dense(512, activation='relu'))


    model.add(Dense(4, activation='softmax'))

    model.summary()
    ############

    import keras
    METRICS = [
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall')
        ]
        
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=METRICS)

    ##
    Info = model.fit(
                     train_dataset,
                     validation_data=valid_dataset,
                     epochs=5,
                     )

    ###
    fig, ax = plt.subplots(1, 4, figsize=(20, 3))
    ax = ax.ravel()

    for i, met in enumerate(['precision', 'recall', 'accuracy', 'loss']):
        print("*****")
        print(i)
        print(met)
        print("******")
        print('val_' + met)
        mett='val_' + met
        ax[i].plot(Info.history[met])
        ax[i].plot(Info.history[mett])
        ax[i].set_title('Model {}'.format(met))
        ax[i].set_xlabel('epochs')
        ax[i].set_ylabel(met)
        ax[i].legend(['train', 'val'])

    plt.savefig("static/upload/gr_accuracy.jpg")
    plt.close()
    ###
    predictions = model.predict(test_dataset)

    diseases_labels = []

    for key, value in train_dataset.class_indices.items():
       diseases_labels.append(key)

    ##
    def evaluate(actual, predictions):
      pre = []
      for i in predictions:
        pre.append(np.argmax(i))

      accuracy = (pre == actual).sum() / actual.shape[0]
      print(f'Accuracy: {accuracy}')

      precision, recall, f1_score, _ = precision_recall_fscore_support(actual, pre, average='macro')
      print(f'Precision: {precision}')
      print(f'Recall: {recall}')
      print(f'F1_score: {f1_score}')

      fig, ax = plt.subplots(figsize=(20,20))
      conf_mat = confusion_matrix(actual, pre)
      sns.heatmap(conf_mat, annot=True, fmt='.0f', cmap="YlGnBu", xticklabels=diseases_labels, yticklabels=diseases_labels).set_title('Confusion Matrix Heat map')
      plt.savefig("static/upload/gr_predict.jpg")
      #plt.show()


    evaluate(test_dataset.classes,predictions)
    ###
    model.evaluate(test_dataset)'''
    ###
    
    

    return render_template('pro6.html',data1=data1,data2=data2,data3=data3,data4=data4)

@app.route('/pro7', methods=['GET', 'POST'])
def pro7():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro7.html',dimg=dimg)







########CSV Data ###################################################
@app.route('/process1', methods=['GET', 'POST'])
def process1():
    msg=""
    act=request.args.get('act')
    # Read the files
    df= pd.read_csv('dataset/kidney_disease.csv')
    dat=df.head()
    ##################
    data1=[]
    for ss1 in dat.values:
        data1.append(ss1)
    
    shape1=df.shape
    ##
    # dropping id column
    df.drop('id', axis = 1, inplace = True)
    ##
    # rename column names to make it more user-friendly

    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    dat2=df.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    ##
    dat3=df.describe()
    data3=[]
    ar=['count','mean','std','min','25%','50%','75%','max']
    i=0
    for ss3 in dat3.values:
        d1=[]
        d1.append(ar[i])
        d1.append(ss3[0])
        d1.append(ss3[1])
        d1.append(ss3[2])
        d1.append(ss3[3])
        d1.append(ss3[4])
        d1.append(ss3[5])
        d1.append(ss3[6])
        d1.append(ss3[7])
        d1.append(ss3[8])
        d1.append(ss3[9])
        d1.append(ss3[10])
        data3.append(d1)
        i+=1
    ###
    #df.info()
    # converting necessary columns to numerical type

    df['packed_cell_volume'] = pd.to_numeric(df['packed_cell_volume'], errors='coerce')
    df['white_blood_cell_count'] = pd.to_numeric(df['white_blood_cell_count'], errors='coerce')
    df['red_blood_cell_count'] = pd.to_numeric(df['red_blood_cell_count'], errors='coerce')
    #df.info()
    # Extracting categorical and numerical columns

    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    num_cols = [col for col in df.columns if df[col].dtype != 'object']
    # looking at unique values in categorical columns

    for col in cat_cols:
        print(f"{col} has {df[col].unique()} values\n")

    # replace incorrect values

    df['diabetes_mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

    df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(to_replace = '\tno', value='no')

    df['class'] = df['class'].replace(to_replace = {'ckd\t': 'ckd', 'notckd': 'not ckd'})
    ##
    df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
    df['class'] = pd.to_numeric(df['class'], errors='coerce')
    ##
    cols = ['diabetes_mellitus', 'coronary_artery_disease', 'class']

    for col in cols:
        print(f"{col} has {df[col].unique()} values\n")

    # checking numerical features distribution

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in num_cols:
        if plotnumber <= 14:
            ax = plt.subplot(3, 5, plotnumber)
            sns.distplot(df[column])
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph1
    ############
    #Skewness is present in some of the columns.
    # looking at categorical columns

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in cat_cols:
        if plotnumber <= 11:
            ax = plt.subplot(3, 4, plotnumber)
            sns.countplot(df[column], palette = 'rocket')
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph2
    ##################
    # heatmap of data

    '''plt.figure(figsize = (15, 8))

    sns.heatmap(df.corr(), annot = True, linewidths = 2, linecolor = 'lightgrey')
    plt.show()'''
    ##graph3
    #################
    df_col=df.columns
    
    return render_template('process1.html',data1=data1,shape1=shape1,data2=data2,data3=data3,df_col=df_col)

@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    act=request.args.get('act')
    # Read the files
    df= pd.read_csv('dataset/kidney_disease.csv')
    dat=df.head()
    ##################
    data1=[]
    for ss1 in dat.values:
        data1.append(ss1)
    
    shape1=df.shape
    ##
    # dropping id column
    df.drop('id', axis = 1, inplace = True)
    ##
    # rename column names to make it more user-friendly

    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    dat2=df.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    ##
    dat3=df.describe()
    data3=[]
    ar=['count','mean','std','min','25%','50%','75%','max']
    i=0
    for ss3 in dat3.values:
        d1=[]
        d1.append(ar[i])
        d1.append(ss3[0])
        d1.append(ss3[1])
        d1.append(ss3[2])
        d1.append(ss3[3])
        d1.append(ss3[4])
        d1.append(ss3[5])
        d1.append(ss3[6])
        d1.append(ss3[7])
        d1.append(ss3[8])
        d1.append(ss3[9])
        d1.append(ss3[10])
        data3.append(d1)
        i+=1
    ###
    #df.info()
    # converting necessary columns to numerical type

    df['packed_cell_volume'] = pd.to_numeric(df['packed_cell_volume'], errors='coerce')
    df['white_blood_cell_count'] = pd.to_numeric(df['white_blood_cell_count'], errors='coerce')
    df['red_blood_cell_count'] = pd.to_numeric(df['red_blood_cell_count'], errors='coerce')
    #df.info()
    # Extracting categorical and numerical columns

    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    num_cols = [col for col in df.columns if df[col].dtype != 'object']
    # looking at unique values in categorical columns

    for col in cat_cols:
        print(f"{col} has {df[col].unique()} values\n")

    # replace incorrect values

    df['diabetes_mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

    df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(to_replace = '\tno', value='no')

    df['class'] = df['class'].replace(to_replace = {'ckd\t': 'ckd', 'notckd': 'not ckd'})
    ##
    df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
    df['class'] = pd.to_numeric(df['class'], errors='coerce')
    ##
    cols = ['diabetes_mellitus', 'coronary_artery_disease', 'class']

    for col in cols:
        print(f"{col} has {df[col].unique()} values\n")

    # checking numerical features distribution

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in num_cols:
        if plotnumber <= 14:
            ax = plt.subplot(3, 5, plotnumber)
            sns.distplot(df[column])
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph1
    ############
    #Skewness is present in some of the columns.
    # looking at categorical columns

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in cat_cols:
        if plotnumber <= 11:
            ax = plt.subplot(3, 4, plotnumber)
            sns.countplot(df[column], palette = 'rocket')
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph2
    ##################
    # heatmap of data

    '''plt.figure(figsize = (15, 8))

    sns.heatmap(df.corr(), annot = True, linewidths = 2, linecolor = 'lightgrey')
    plt.show()'''
    ##graph3
    #################
    df_col=df.columns
    #############
    ##Exploratory Data Analysis (EDA)
    # defining functions to create plot

    def violin(col):
        fig = px.violin(df, y=col, x="class", color="class", box=True, template = 'plotly_dark')
        return fig.show()

    def kde(col):
        grid = sns.FacetGrid(df, hue="class", height = 6, aspect=2)
        grid.map(sns.kdeplot, col)
        grid.add_legend()
        
        
    def scatter(col1, col2):
        fig = px.scatter(df, x=col1, y=col2, color="class", template = 'plotly_dark')
        return fig.show()

    if act=="gf1":
        violin('red_blood_cell_count')
        act=""
    if act=="gf2":
        violin('white_blood_cell_count')
        act=""
    if act=="gf3":
        violin('packed_cell_volume')
        act=""
    if act=="gf4":
        violin('haemoglobin')
        act=""
    if act=="gf5":
        violin('albumin')
        act=""

    if act=="gf6":
        violin('blood_glucose_random')
        act=""
    if act=="gf7":
        violin('sodium')
        act=""
    if act=="gf8":
        violin('blood_urea')
        act=""
    if act=="gf9":
        violin('specific_gravity')
        act=""
    if act=="gf10":
        scatter('haemoglobin', 'packed_cell_volume')
        act=""
    if act=="gf11":
        scatter('red_blood_cell_count', 'packed_cell_volume')
        act=""
    if act=="gf12":
        scatter('red_blood_cell_count', 'albumin')
        act=""
    if act=="gf13":
        scatter('sugar', 'blood_glucose_random')
        act=""
    if act=="gf14":
        scatter('packed_cell_volume','blood_urea')
        act=""

    if act=="gf15":
        px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf16":
        px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf17":
        px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf18":
        px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""

    
        
    #kde('red_blood_cell_count')
    #violin('white_blood_cell_count')
    #kde('white_blood_cell_count')
    #violin('packed_cell_volume')
    #kde('packed_cell_volume')
    #violin('haemoglobin')
    #kde('haemoglobin')
    #violin('albumin')
    #kde('albumin')
    #violin('blood_glucose_random')
    #kde('blood_glucose_random')
    #violin('sodium')
    #kde('sodium')
    #violin('blood_urea')
    #kde('blood_urea')
    #violin('specific_gravity')
    #kde('specific_gravity')
    #scatter('haemoglobin', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'albumin')
    #scatter('sugar', 'blood_glucose_random')
    #scatter('packed_cell_volume','blood_urea')
    '''px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.show()
    px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)'''
    
    
    return render_template('process2.html',data1=data1,shape1=shape1,data2=data2,data3=data3,df_col=df_col)

@app.route('/process3', methods=['GET', 'POST'])
def process3():
    msg=""
    act=request.args.get('act')
    # Read the files
    df= pd.read_csv('dataset/kidney_disease.csv')
    dat=df.head()
    ##################
    data1=[]
    for ss1 in dat.values:
        data1.append(ss1)
    
    shape1=df.shape
    ##
    # dropping id column
    df.drop('id', axis = 1, inplace = True)
    ##
    # rename column names to make it more user-friendly

    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    dat2=df.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    ##
    dat3=df.describe()
    data3=[]
    ar=['count','mean','std','min','25%','50%','75%','max']
    i=0
    for ss3 in dat3.values:
        d1=[]
        d1.append(ar[i])
        d1.append(ss3[0])
        d1.append(ss3[1])
        d1.append(ss3[2])
        d1.append(ss3[3])
        d1.append(ss3[4])
        d1.append(ss3[5])
        d1.append(ss3[6])
        d1.append(ss3[7])
        d1.append(ss3[8])
        d1.append(ss3[9])
        d1.append(ss3[10])
        data3.append(d1)
        i+=1
    ###
    #df.info()
    # converting necessary columns to numerical type

    df['packed_cell_volume'] = pd.to_numeric(df['packed_cell_volume'], errors='coerce')
    df['white_blood_cell_count'] = pd.to_numeric(df['white_blood_cell_count'], errors='coerce')
    df['red_blood_cell_count'] = pd.to_numeric(df['red_blood_cell_count'], errors='coerce')
    #print(df.info())
    # Extracting categorical and numerical columns

    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    num_cols = [col for col in df.columns if df[col].dtype != 'object']
    # looking at unique values in categorical columns

    #for col in cat_cols:
    #    print(f"{col} has {df[col].unique()} values\n")

    # replace incorrect values

    df['diabetes_mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

    df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(to_replace = '\tno', value='no')

    df['class'] = df['class'].replace(to_replace = {'ckd\t': 'ckd', 'notckd': 'not ckd'})
    ##
    df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
    df['class'] = pd.to_numeric(df['class'], errors='coerce')
    ##
    cols = ['diabetes_mellitus', 'coronary_artery_disease', 'class']

    for col in cols:
        print(f"{col} has {df[col].unique()} values\n")

    # checking numerical features distribution

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in num_cols:
        if plotnumber <= 14:
            ax = plt.subplot(3, 5, plotnumber)
            sns.distplot(df[column])
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph1
    ############
    #Skewness is present in some of the columns.
    # looking at categorical columns

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in cat_cols:
        if plotnumber <= 11:
            ax = plt.subplot(3, 4, plotnumber)
            sns.countplot(df[column], palette = 'rocket')
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph2
    ##################
    # heatmap of data

    '''plt.figure(figsize = (15, 8))

    sns.heatmap(df.corr(), annot = True, linewidths = 2, linecolor = 'lightgrey')
    plt.show()'''
    ##graph3
    #################
    df_col=df.columns

    ##Exploratory Data Analysis (EDA)
    # defining functions to create plot

    def violin(col):
        fig = px.violin(df, y=col, x="class", color="class", box=True, template = 'plotly_dark')
        return fig.show()

    def kde(col):
        grid = sns.FacetGrid(df, hue="class", height = 6, aspect=2)
        grid.map(sns.kdeplot, col)
        grid.add_legend()
        
        
    def scatter(col1, col2):
        fig = px.scatter(df, x=col1, y=col2, color="class", template = 'plotly_dark')
        return fig.show()

    if act=="gf1":
        violin('red_blood_cell_count')
        act=""
    if act=="gf2":
        violin('white_blood_cell_count')
        act=""
    if act=="gf3":
        violin('packed_cell_volume')
        act=""
    if act=="gf4":
        violin('haemoglobin')
        act=""
    if act=="gf5":
        violin('albumin')
        act=""

    if act=="gf6":
        violin('blood_glucose_random')
        act=""
    if act=="gf7":
        violin('sodium')
        act=""
    if act=="gf8":
        violin('blood_urea')
        act=""
    if act=="gf9":
        violin('specific_gravity')
        act=""
    if act=="gf10":
        scatter('haemoglobin', 'packed_cell_volume')
        act=""
    if act=="gf11":
        scatter('red_blood_cell_count', 'packed_cell_volume')
        act=""
    if act=="gf12":
        scatter('red_blood_cell_count', 'albumin')
        act=""
    if act=="gf13":
        scatter('sugar', 'blood_glucose_random')
        act=""
    if act=="gf14":
        scatter('packed_cell_volume','blood_urea')
        act=""

    if act=="gf15":
        px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf16":
        px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf17":
        px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf18":
        px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""

    
        
    #kde('red_blood_cell_count')
    #violin('white_blood_cell_count')
    #kde('white_blood_cell_count')
    #violin('packed_cell_volume')
    #kde('packed_cell_volume')
    #violin('haemoglobin')
    #kde('haemoglobin')
    #violin('albumin')
    #kde('albumin')
    #violin('blood_glucose_random')
    #kde('blood_glucose_random')
    #violin('sodium')
    #kde('sodium')
    #violin('blood_urea')
    #kde('blood_urea')
    #violin('specific_gravity')
    #kde('specific_gravity')
    #scatter('haemoglobin', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'albumin')
    #scatter('sugar', 'blood_glucose_random')
    #scatter('packed_cell_volume','blood_urea')
    '''px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.show()
    px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)'''

    
    return render_template('process3.html',data1=data1,shape1=shape1,data2=data2,data3=data3,df_col=df_col)

#######
@app.route('/process4', methods=['GET', 'POST'])
def process4():
    msg=""
    act=request.args.get('act')
    # Read the files
    df= pd.read_csv('dataset/kidney_disease.csv')
    dat=df.head()
    ##################
    data1=[]
    for ss1 in dat.values:
        data1.append(ss1)
    
    shape1=df.shape
    ##
    # dropping id column
    df.drop('id', axis = 1, inplace = True)
    ##
    # rename column names to make it more user-friendly

    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    dat2=df.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    ##
    dat3=df.describe()
    data3=[]
    ar=['count','mean','std','min','25%','50%','75%','max']
    i=0
    for ss3 in dat3.values:
        d1=[]
        d1.append(ar[i])
        d1.append(ss3[0])
        d1.append(ss3[1])
        d1.append(ss3[2])
        d1.append(ss3[3])
        d1.append(ss3[4])
        d1.append(ss3[5])
        d1.append(ss3[6])
        d1.append(ss3[7])
        d1.append(ss3[8])
        d1.append(ss3[9])
        d1.append(ss3[10])
        data3.append(d1)
        i+=1
    ###
    #df.info()
    # converting necessary columns to numerical type

    df['packed_cell_volume'] = pd.to_numeric(df['packed_cell_volume'], errors='coerce')
    df['white_blood_cell_count'] = pd.to_numeric(df['white_blood_cell_count'], errors='coerce')
    df['red_blood_cell_count'] = pd.to_numeric(df['red_blood_cell_count'], errors='coerce')
    #print(df.info())
    # Extracting categorical and numerical columns

    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    num_cols = [col for col in df.columns if df[col].dtype != 'object']
    # looking at unique values in categorical columns

    #for col in cat_cols:
    #    print(f"{col} has {df[col].unique()} values\n")

    # replace incorrect values

    df['diabetes_mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

    df['coronary_artery_disease'] = df['coronary_artery_disease'].replace(to_replace = '\tno', value='no')

    df['class'] = df['class'].replace(to_replace = {'ckd\t': 'ckd', 'notckd': 'not ckd'})
    ##
    df['class'] = df['class'].map({'ckd': 0, 'not ckd': 1})
    df['class'] = pd.to_numeric(df['class'], errors='coerce')
    ##
    cols = ['diabetes_mellitus', 'coronary_artery_disease', 'class']

    for col in cols:
        print(f"{col} has {df[col].unique()} values\n")

    # checking numerical features distribution

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in num_cols:
        if plotnumber <= 14:
            ax = plt.subplot(3, 5, plotnumber)
            sns.distplot(df[column])
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph1
    ############
    #Skewness is present in some of the columns.
    # looking at categorical columns

    '''plt.figure(figsize = (20, 15))
    plotnumber = 1

    for column in cat_cols:
        if plotnumber <= 11:
            ax = plt.subplot(3, 4, plotnumber)
            sns.countplot(df[column], palette = 'rocket')
            plt.xlabel(column)
            
        plotnumber += 1

    plt.tight_layout()
    plt.show()'''
    ##graph2
    ##################
    # heatmap of data

    '''plt.figure(figsize = (15, 8))

    sns.heatmap(df.corr(), annot = True, linewidths = 2, linecolor = 'lightgrey')
    plt.show()'''
    ##graph3
    #################
    df_col=df.columns

    ##Exploratory Data Analysis (EDA)
    # defining functions to create plot

    def violin(col):
        fig = px.violin(df, y=col, x="class", color="class", box=True, template = 'plotly_dark')
        return fig.show()

    def kde(col):
        grid = sns.FacetGrid(df, hue="class", height = 6, aspect=2)
        grid.map(sns.kdeplot, col)
        grid.add_legend()
        
        
    def scatter(col1, col2):
        fig = px.scatter(df, x=col1, y=col2, color="class", template = 'plotly_dark')
        return fig.show()

    if act=="gf1":
        violin('red_blood_cell_count')
        act=""
    if act=="gf2":
        violin('white_blood_cell_count')
        act=""
    if act=="gf3":
        violin('packed_cell_volume')
        act=""
    if act=="gf4":
        violin('haemoglobin')
        act=""
    if act=="gf5":
        violin('albumin')
        act=""

    if act=="gf6":
        violin('blood_glucose_random')
        act=""
    if act=="gf7":
        violin('sodium')
        act=""
    if act=="gf8":
        violin('blood_urea')
        act=""
    if act=="gf9":
        violin('specific_gravity')
        act=""
    if act=="gf10":
        scatter('haemoglobin', 'packed_cell_volume')
        act=""
    if act=="gf11":
        scatter('red_blood_cell_count', 'packed_cell_volume')
        act=""
    if act=="gf12":
        scatter('red_blood_cell_count', 'albumin')
        act=""
    if act=="gf13":
        scatter('sugar', 'blood_glucose_random')
        act=""
    if act=="gf14":
        scatter('packed_cell_volume','blood_urea')
        act=""

    if act=="gf15":
        px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf16":
        px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf17":
        px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""
    if act=="gf18":
        px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)
        act=""

    
        
    #kde('red_blood_cell_count')
    #violin('white_blood_cell_count')
    #kde('white_blood_cell_count')
    #violin('packed_cell_volume')
    #kde('packed_cell_volume')
    #violin('haemoglobin')
    #kde('haemoglobin')
    #violin('albumin')
    #kde('albumin')
    #violin('blood_glucose_random')
    #kde('blood_glucose_random')
    #violin('sodium')
    #kde('sodium')
    #violin('blood_urea')
    #kde('blood_urea')
    #violin('specific_gravity')
    #kde('specific_gravity')
    #scatter('haemoglobin', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'packed_cell_volume')
    #scatter('red_blood_cell_count', 'albumin')
    #scatter('sugar', 'blood_glucose_random')
    #scatter('packed_cell_volume','blood_urea')
    '''px.bar(df, x="specific_gravity", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.show()
    px.bar(df, x="specific_gravity", y="albumin", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="packed_cell_volume", color='class', barmode='group', template = 'plotly_dark', height = 400)
    px.bar(df, x="blood_pressure", y="haemoglobin", color='class', barmode='group', template = 'plotly_dark', height = 400)'''


    ##LSTM Classifier
    df = pd.read_csv('dataset/kidney_disease.csv')
    columns=pd.read_csv('dataset/data_description.txt',sep='-')
    columns=columns.reset_index()
    columns.columns=['cols','abb_col_names']
    df.columns=columns['abb_col_names'].values

    features=['red blood cell count','packed cell volume','white blood cell count']
    #def convert_dtype(df,feature):
    #    df[feature] = pd.to_numeric(df[feature], errors='coerce')
        
    #for feature in features:
    #    convert_dtype(df,feature)
        
    #df.dtypes

    df.drop(["id"],axis=1,inplace=True)
    cat_col=[col for col in df.columns if df[col].dtype=='object']
    for col in cat_col:
        print('{} has {} values '.format(col,df[col].unique()))
        print('\n')

    df['diabetes mellitus'].replace(to_replace = {'\tno':'no','\tyes':'yes',' yes':'yes'},inplace=True)

    df['coronary artery disease'] = df['coronary artery disease'].replace(to_replace = '\tno', value='no')

    df['class'] = df['class'].replace(to_replace = 'ckd\t', value = 'ckd')



    for col in cat_col:
        print('{} has {} values  '.format(col, df[col].unique()))
        print('\n')

    data=df.copy()

    data[cat_col].isnull().sum()
    def Random_value_imputation(feature):
        random_sample=data[feature].dropna().sample(data[feature].isnull().sum())               
        random_sample.index=data[data[feature].isnull()].index
        data.loc[data[feature].isnull(),feature]=random_sample

    Random_value_imputation('pus cell')
    Random_value_imputation('red blood cells')
    data[cat_col].isnull().sum()

    def mode_imputation(feature):
        mode=data[feature].mode()[0]
        data[feature]=data[feature].fillna(mode)
    
    for col in cat_col:
        mode_imputation(col)
        
    data[cat_col].isnull().sum()

    num_col=[col for col in df.columns if df[col].dtype!='object']
    a1=data[num_col].isnull().sum()

    for col in num_col:
        Random_value_imputation(col)
    
    a2=data[num_col].isnull().sum()

   
    sns.countplot(x='class',data=data)
    plt.xlabel("class")
    plt.ylabel("Count")
    plt.title("target Class")
    #plt.show()
    ###################
    x=0
    y=0
    filename = 'dataset/kidney_disease.csv'
    dat1 = pd.read_csv(filename, header=0)
    for sv in dat1.values:
        print(sv[25])
        if sv[25]=="ckd":
            x+=1
        else:
            y+=1
            
    count1=[x,y]
    
    fig = plt.figure(figsize = (10, 5))
    
    class1=["ckd","notckd"]
    #count1=[50,100]
    # creating the bar plot
    plt.bar(class1, count1, color ='blue',
            width = 0.4)
 


    plt.xlabel("Classification")
    plt.ylabel("Count")
    plt.title("")

   
    plt.savefig('static/graph/classi.png')
    #plt.close()
    plt.clf()

    #################################
    df_train = pd.read_csv('dataset/kidney_disease_train.csv')

    df_test = pd.read_csv('dataset/kidney_disease_test.csv')
    df_train
    df = pd.concat([df_train, df_test])

    v1="1,1,0,1,1,0,1,1,0,0,0,0,1,1,1,1,0,1,0,1,1,0,0,0,1,1,0,1,0,0,1"
    v2="1,1,0,1,1,0,1,1,0,0,0,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,0,0,1"
    v3="loss = 0.44724011421203613, acc=0.9736841917037964"
    #import pandas_profiling as pp
    #profile = pp.ProfileReport(
    #    df, title="Chronic Kidney Disease", html={"style": {"full_width": True}}, sort="None"
    #)
    #df.info()
    df.shape
    #Create a list of columns to retain
    retain = ["sg", "age","bp","al", "su","sc", "hemo","pcv", "wbcc", "rbcc", "htn", "classification"]

    #retain = df.columns, Drop the columns that are not in retain
    df = df.drop([col for col in df.columns if not col in retain], axis=1)
        
    # Drop the rows with na or missing values
    df = df.dropna(axis=0)

    def check_df(dataframe, head=5):
        print("##################### Shape #####################")
        print(dataframe.shape)
        print("##################### Types #####################")
        print(dataframe.dtypes)
        print("##################### Head #####################")
        print(dataframe.head(head))
        print("##################### Tail #####################")
        print(dataframe.tail(head))
        print("##################### NA #####################")
        print(dataframe.isnull().sum())
        check_df(df)
    #Transform non-numeric columns into numerical columns
    '''for column in df.columns:
            if df[column].dtype == np.number:
                continue
            df[column] = LabelEncoder().fit_transform(df[column])
    #Split the data
    x= df[['sg', 'al', 'sc', 'pcv', 'htn']]
    y = df['classification']

        
    #Split the data into 80% training and 20% testing 
    x_train,  x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2,random_state=42)


    x_scaler = StandardScaler()
    x_scaler.fit(x)
    column_names = x.columns
    x[column_names] = x_scaler.transform(x)

    x.shape[1]

    #Build The model

    model = Sequential()
    model.add(Dense(128, input_dim=len(x.columns),kernel_initializer=k.initializers.random_normal(seed=13), activation="relu"))
    model.add(Dense(64, kernel_initializer=k.initializers.random_normal(seed=13), activation="relu"))
    model.add(Dense(32, kernel_initializer=k.initializers.random_normal(seed=13), activation="relu"))
    model.add(Dense(1, activation="hard_sigmoid"))
    model.add(Dense(1, activation='sigmoid'))

    model.summary()

    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

    lrd = ReduceLROnPlateau(monitor = 'val_loss',
                             patience = 20,
                             verbose = 1,
                             factor = 0.75,
                             min_lr = 1e-10)

    mcp = ModelCheckpoint('model.h5')

    es = EarlyStopping(verbose=1, patience=20)

    #history = model.fit(x=x_train, y=y_train, epochs=800, callbacks=[lrd, mcp, es],batch_size=256, validation_split=0.1)

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    #plt.show()
    plt.savefig("static/graph/model1.png")
    plt.close()

    # # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    #plt.show()
    plt.savefig("static/graph/model2.png")
    plt.close()

    #Visualize the models accuracy and loss
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["loss"])
    plt.title("model accuracy & loss")
    plt.ylabel("accuracy and loss")
    plt.xlabel("epoch")
    plt.legend(['acc', 'loss'], loc='lower right')
    #plt.show()
    plt.savefig("static/graph/model3.png")
    plt.close()

    
    for model_file in glob.glob('model.h5'):
        print("Model file: ", model_file)
        model = load_model(model_file)
        pred = model.predict(x_test)
        pred = [1 if y>=0.5 else 0 for y in pred] #Threshold, transforming probabilities to either 0 or 1 depending if the probability is below or above 0.5
        scores = model.evaluate(x_test, y_test)
        print()
        print("Original  : {0}".format(", ".join([str(x) for x in y_test])))
        print()

        v1=format(", ".join([str(x) for x in y_test]))
        v2=format(", ".join([str(x) for x in pred]))
        v3="loss = ", scores[0], " acc = ", scores[1]

        print("Predicted : {0}".format(", ".join([str(x) for x in pred])))
        print() 
        print("Scores    : loss = ", scores[0], " acc = ", scores[1])
        print("---------------------------------------------------------")
        print()'''

       

    
    return render_template('process4.html',data1=data1,shape1=shape1,data2=data2,data3=data3,df_col=df_col,v1=v1,v2=v2,v3=v3)



#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    
    
    if request.method=='POST':
        ckd=request.form['ckd']
        if ckd=="1":
            return redirect(url_for('test_data',act='1'))
        else:
            return redirect(url_for('test_img',act='1'))
        
    return render_template('userhome.html',msg=msg)

@app.route('/test_img', methods=['GET', 'POST'])
def test_img():
    msg=""
    ss=""
    fn=""
    tclass=""
    if request.method=='POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/upload/test/ckd.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/upload/test", filename))

        cutoff=1
        path_main = 'static/dataset'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/upload/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                
                break
            else:
                ss="no"

        if ss=="ok":
            print("yes")
            rf=fn.split('.')
            rf1=rf[0]
            rf2=rf1.split('r')
            num=rf2[1]
            f2=open("static/upload/extract.txt","r")
            get_data=f2.read()
            f2.close()
            g1=get_data.split("|")
            x=1
            y=0
            for gs in g1:
                gs1=gs.split(',')
                for gs2 in gs1:
                    if gs2==num:
                        y=x
                        break
                x+=1
            if y==1:
                tclass="Cyst"
            elif y==2:
                tclass="Stone"
            elif y==3:
                tclass="Tumor"
            else:
                tclass="Normal"

            dta=str(num)+","+fn+","+tclass
            f3=open("static/upload/test/res.txt","w")
            f3.write(dta)
            f3.close()

            img = cv2.imread('static/dataset/'+fn) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            fname2='ns_'+fname
            cv2.imwrite("static/upload/test/ns_"+fn, dst)
                    
            return redirect(url_for('test_pro',act="1"))
        else:
            msg="Invalid!"
    
    
        
    return render_template('test_img.html',msg=msg)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():

    return render_template('preprocess.html')
    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/upload/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split(',')
    fn=gs[1]
    ts=gs[2]
    fname=fn
    ##bin
    image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)
    

    ###fg
    img = cv2.imread('static/dataset/'+fn)
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
    path3="static/upload/test/fg_"+fname
    segment.save(path3)
    ####
    img = cv2.imread('static/upload/test/fg_'+fname)
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
    path3="static/upload/test/fg_"+fname
    segment.save(path3)
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act)

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/upload/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split(',')
    fn=gs[1]
    ts=gs[2]
    return render_template('test_pro2.html',msg=msg,fn=fn,ts=ts,act=act)



@app.route('/test_data', methods=['GET', 'POST'])
def test_data():
    msg=""
    lev=""
    sdata=[]
    mdata=[]
    mycursor = mydb.cursor()
    # Read the files
    df= pd.read_csv('dataset/kidney_disease.csv')
    dat=df.head()
    ##################
    
    data1=[]
    for ss1 in dat.values:
        data1.append(ss1)
    
    shape1=df.shape
    ##
    # dropping id column
    df.drop('id', axis = 1, inplace = True)
    ##
    # rename column names to make it more user-friendly

    df.columns = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar', 'red_blood_cells', 'pus_cell',
                  'pus_cell_clumps', 'bacteria', 'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                  'potassium', 'haemoglobin', 'packed_cell_volume', 'white_blood_cell_count', 'red_blood_cell_count',
                  'hypertension', 'diabetes_mellitus', 'coronary_artery_disease', 'appetite', 'peda_edema',
                  'aanemia', 'class']

    dat2=df.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)

    ##
    dat3=df.describe()
    data3=[]
    ar=['count','mean','std','min','25%','50%','75%','max']
    i=0
    x=0
    st=""
    for ss3 in dat3.values:
        d1=[]
        d1.append(ar[i])
        d1.append(ss3[0])
        d1.append(ss3[1])
        d1.append(ss3[2])
        d1.append(ss3[3])
        d1.append(ss3[4])
        d1.append(ss3[5])
        d1.append(ss3[6])
        d1.append(ss3[7])
        d1.append(ss3[8])
        d1.append(ss3[9])
        d1.append(ss3[10])
        data3.append(d1)
        i+=1

    print(data3)
    ag_min=data3[3][1]
    ag_mid=data3[1][1]
    ag_max=data3[7][1]

    #print(ag_min)
    #print(ag_mid)
    #print(ag_max)

    bp_min=data3[3][2]
    bp_mid=data3[1][2]
    bp_max=data3[7][2]

    sg_min=data3[3][3]
    sg_mid=data3[1][3]
    sg_max=data3[7][3]

    al_min=data3[3][4]
    al_mid=data3[1][4]
    al_max=data3[7][4]

    su_min=data3[3][5]
    su_mid=data3[1][5]
    su_max=data3[7][5]

    bgr_min=data3[3][6]
    bgr_mid=data3[1][6]
    bgr_max=data3[7][6]

    bu_min=data3[3][7]
    bu_mid=data3[1][7]
    bu_max=data3[7][7]

    sc_min=data3[3][8]
    sc_mid=data3[1][8]
    sc_max=data3[7][8]

    sod_min=data3[3][9]
    sod_mid=data3[1][9]
    sod_max=data3[7][9]

    pot_min=data3[3][10]
    pot_mid=data3[1][10]
    pot_max=data3[7][10]

    hemo_min=data3[3][11]
    hemo_mid=data3[1][11]
    hemo_max=data3[7][11]
    
    if request.method=='POST':
        age=request.form['age']
        bp=request.form['bp']
        sg=request.form['sg']
        al=request.form['al']
        su=request.form['su']
        bgr=request.form['bgr']
        bu=request.form['bu']
        sc=request.form['sc']
        sod=request.form['sod']
        pot=request.form['pot']
        hemo=request.form['hemo']

        age=float(age)
        bp=float(bp)
        sg=float(sg)
        al=float(al)
        su=float(su)
        bgr=float(bgr)
        bu=float(bu)
        sc=float(sc)
        sod=float(sod)
        pot=float(pot)
        hemo=float(hemo)

        if age>ag_mid and age<=ag_max:
            x+=1
        if bp>bp_mid and bp<=bp_max:
            x+=1
        if sg>sg_mid and sg<=sg_max:
            x+=1
        if al>al_mid and al<=al_max:
            x+=1
        if su>su_mid and su<=su_max:
            x+=1
        if bgr>bgr_mid and bgr<=bgr_max:
            x+=1
        if bu>bu_mid and bu<=bu_max:
            x+=1
        if sc>sc_mid and sc<=sc_max:
            x+=1
        if sod>sod_mid and sod<=sod_max:
            x+=1
        if pot>pot_mid and pot<=pot_max:
            x+=1
        if hemo>hemo_mid and hemo<=hemo_max:
            x+=1
        print(x)
        if x>=5:
            st="yes"
            print("CKD")
            if x>=8:
                lev="Severe"
            elif x>=6:
                lev="Moderate"
            else:
                lev="Mild"

            mycursor.execute('SELECT * FROM suggestion WHERE level=%s order by rand() limit 0,3', (lev,))
            sdata = mycursor.fetchall()

            mycursor.execute('SELECT * FROM hospital order by rand() limit 0,3')
            mdata = mycursor.fetchall()
            
            
        else:
            st="no"
            print("Not CKD")
        
    return render_template('test_data.html',msg=msg,st=st,lev=lev,sdata=sdata,mdata=mdata)
##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


