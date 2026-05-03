import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog
from tkinter import messagebox
import cv2
import os
import time
import threading
import glob
import tkinter as tk
from tkinter import ttk
import PIL.Image, PIL.ImageTk
from tkinter import *
from PIL import Image
from PIL import ImageTk
root = Tk()
##win1 = Tk()
##win2 = Tk()

canvas = tk.Canvas(root, height=600, width=600)
s = "upload/eye.jpg"
global sh
sh = 0
f = 1
rid = 0
u1 = 1
sd = ""
def train():
    canvas = Canvas(root, bg="lightblue",height=600,width=600)
    canvas.pack()
    #canvas.place(x=0, y=150)
    
    
    
    
    lt1 = Label(root, text='Training Process',bg='lightblue', fg='green', font=("Helvetica", 18))
    lt1.pack()
    lt1.place(x=220, y=10)
    b1 = Button(root, text='Select Data Folder', command=uploaddir)
    b1.pack()
    b1.place(x=220, y=40)

    

def uploaddir():
    
    global sd
    dirname = filedialog.askdirectory()
    sd = dirname
    print(dirname)
    #files=os.listdir(dirname)
    #print(files)
    #lt11 = Label(root, text=sd,bg='lightblue', fg='blue', font=("Helvetica", 14))
    #lt11.pack()
    #lt11.place(x=100, y=65)
    b13 = Button(root, text='Training Process', command=tprocess)
    b13.pack()
    b13.place(x=410, y=40)
##    b12 = Button(root, text='Start Process', command=savefile)
##    b12.pack()
##    b12.place(x=320, y=40)

## def savefile():
    
##    print(sd)
##    files=os.listdir(sd)
##    fn = 1
##    for fx in (files):
##        #print(fx)
##        fpath=sd+"/"+fx
##        mm = PIL.Image.open(fpath)
##        fname="r"+str(fn)+".jpg"
##        #print(fname)
##        #mm.save("dataset/"+fname)
##        fn += 1
##    #messagebox.showinfo("Image","Saved Successfully")
##    
##    

def tprocess():
    
    totdata=4
    lt11 = Label(root, text='Training process going..................................',bg='lightblue', fg='blue', font=("Helvetica", 14))
    lt11.pack()
    lt11.place(x=100, y=100)
    j = 1
    while j<=totdata:
        fnm = "r"+str(j)+".jpg"
        swimg = "Image"+str(j)
        

        #canvas = Canvas(root, bg="lightblue",height=30,width=600)
        #canvas.pack()
        #canvas.place(x=0, y=160)
    
        ltg = Label(root, text=swimg,bg='green', fg='yellow', font=("Helvetica", 14))
        ltg.pack()
        ltg.place(x=100, y=130)
        i = 1
        while i <= 5:
            if i==1:
                word='Training process-------------------Resize'
            elif i==2:
                word='Training process----------------Grayscale'
            elif i==3:
                word='Training process----------------------Noise'
            elif i==4:
                word='Training process----Feature Extraction'
            else:
                print("")
                #word='Training Completed...........................................'
                
            lt11 = Label(root, text=word,bg='lightblue', fg='blue', font=("Helvetica", 14))
            lt11.pack()
            lt11.place(x=100, y=160)
            #while k <= 1:
            
            path2 = "dataset/"+fnm
            if i==1:
                
                mm2 = PIL.Image.open(path2)
                rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                img2 = PIL.ImageTk.PhotoImage(rz)
                panel2 = Label(root, image = img2)
                panel2.image = img2 # keep a reference!
                panel2.pack()
                panel2.place(x=50,y=200)
            elif i==2:
                mm2 = PIL.Image.open(path2).convert('L')
                #mm2 = PIL.Image.open(path2)
                rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                rz.save("upload/grayscale.jpg")
                img2 = PIL.ImageTk.PhotoImage(rz)
                panel2 = Label(root, image = img2)
                panel2.image = img2 # keep a reference!
                panel2.pack()
                panel2.place(x=50,y=200)
            elif i==3:
                img = cv2.imread('upload/grayscale.jpg') 
                dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
                cv2.imwrite("upload/noise.jpg", dst)

                mm2 = PIL.Image.open("upload/noise.jpg")
                img2 = PIL.ImageTk.PhotoImage(mm2)
                panel2 = Label(root, image = img2)
                panel2.image = img2 # keep a reference!
                panel2.pack()
                panel2.place(x=50,y=200)  
            elif i==4:
                image = cv2.imread("upload/grayscale.jpg")
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edged = cv2.Canny(gray, 50, 100)
                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                edged = Image.fromarray(edged)
                image = ImageTk.PhotoImage(image)
                edged = ImageTk.PhotoImage(edged)
                panel2 = Label(root, image = edged)
                panel2.image = edged # keep a reference!
                panel2.pack()
                panel2.place(x=50,y=200)
                

            if i<5:
                canvas.update()
                time.sleep(1)
            i += 1
        j += 1    
        if totdata<j:
            messagebox.showinfo("Image","Training Process completed & Training File created")

    
    
    
    
    
    
def testing():
    print("hsi")

    canvas = Canvas(root, bg="lightblue",height=600,width=600)
    canvas.pack() 

    lt111 = Label(root, text='Testing Process',bg='lightblue', fg='green', font=("Helvetica", 14))
    lt111.pack()
    lt111.place(x=250, y=30)
    

    b11 = Button(root, text='Upload Image', command=upload1)
    b11.pack()
    b11.place(x=280, y=60)
    
    
    
def upload1():
    global s
    global f
    global rid
    canvas = Canvas(root, bg="lightblue",height=600,width=600)
    canvas.pack() 
    sh = 1
    #a1 = Label(win2, text='==========Image==========')
    #a1.pack()
    #a1.place(x=50, y=10)
    panel = Label(root, image = None)
    panel.image = None # keep a reference!
    panel.pack()
    #root.configure(background='green')
    ftypes = [
        ('jpg files', '*.jpg'),
        ('jpeg/png files', '*.jpeg;*.png'),  # semicolon trick
        ('gif files', '*.gif'),
    ]
    
    filename = filedialog.askopenfilename(filetypes=ftypes)
    mm = PIL.Image.open(filename)
    mm.save("upload/m1.jpg")
    ####
    
    u = 1
    
    original = cv2.imread("upload/m1.jpg")
    while u <= 50:
        mg = "r"+str(u)+".jpg"
        #print(mg)
        duplicate = cv2.imread("dataset/"+mg)


        if original.shape == duplicate.shape:
            #print("m"+str(u)+"incorrect")
            difference = cv2.subtract(original, duplicate)
            b, g, r = cv2.split(difference)
            #print(str(b)+"----"+str(g)+"----"+str(r))

            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("m"+str(u)+"incorrect")
                
                
            else:
                f += 1
                rid=u
                print("m"+str(u)+"correct")
           
                    
        #cv2.imshow("Original", original)
        #cv2.imshow("Duplicate", duplicate)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        u += 1
        
    mm1 = PIL.Image.open("upload/m1.jpg")
    mm1 = mm1.resize((300,300), PIL.Image.ANTIALIAS)
    mm1.save("upload/m1.jpg")
    print("rid1==="+str(rid))
    if f>=1:
        testprocess()
 
def testprocess():
    print("rid2=="+str(rid))
    i = 1
    while i <= 5:
        if i==1:
            word='Testing process------------------Resize'
        elif i==2:
            word='Testing process----------------Grayscale'
        elif i==3:
            word='Testing process----------------------Noise'
        elif i==4:
            word='Testing process----Feature Extraction'
        else:
            print("")
            #word='Testing Completed...........................................'
            
        lt11 = Label(root, text=word,bg='lightblue', fg='blue', font=("Helvetica", 14))
        lt11.pack()
        lt11.place(x=100, y=160)
        #while k <= 1:
        
        path2 = "upload/m1.jpg"
        if i==1:
            
            mm2 = PIL.Image.open(path2)
            rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
            img2 = PIL.ImageTk.PhotoImage(rz)
            panel2 = Label(root, image = img2)
            panel2.image = img2 # keep a reference!
            panel2.pack()
            panel2.place(x=50,y=200)
        elif i==2:
            mm2 = PIL.Image.open(path2).convert('L')
            #mm2 = PIL.Image.open(path2)
            rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
            rz.save("upload/gray.jpg")
            img2 = PIL.ImageTk.PhotoImage(rz)
            panel2 = Label(root, image = img2)
            panel2.image = img2 # keep a reference!
            panel2.pack()
            panel2.place(x=50,y=200)
        elif i==3:
            img = cv2.imread('upload/gray.jpg') 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            cv2.imwrite("upload/noi.jpg", dst)

            mm2 = PIL.Image.open("upload/noise.jpg")
            img2 = PIL.ImageTk.PhotoImage(mm2)
            panel2 = Label(root, image = img2)
            panel2.image = img2 # keep a reference!
            panel2.pack()
            panel2.place(x=50,y=200)  
        elif i==4:
            image = cv2.imread("upload/gray.jpg")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            image = ImageTk.PhotoImage(image)
            edged = ImageTk.PhotoImage(edged)
            panel2 = Label(root, image = edged)
            panel2.image = edged # keep a reference!
            panel2.pack()
            panel2.place(x=50,y=200)
            

        if i<5:
            canvas.update()
            time.sleep(1)
        i += 1
    
    messagebox.showinfo("Image","Testing Completed")
    classi()

        
def compare1():
    global u1
    
    
    #print("rid="+str(rid)+" f="+str(f))
    #threading.Timer(5, compare1).start()
    while u1 <= 50:
        
        path = "upload/m1.jpg"
        img = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
        panel = Label(root, image = img)
        panel.image = img # keep a reference!
        panel.pack()
        panel.place(x=50,y=50)

        mg1 = "r"+str(u1)+".jpg"
        path2 = "dataset/"+mg1
        mm2 = PIL.Image.open(path2)
        mm2 = mm2.resize((300,300), PIL.Image.ANTIALIAS)
        mm2.save("upload/y.jpg")
        img2 = PIL.ImageTk.PhotoImage(PIL.Image.open("upload/y.jpg"))
        panel2 = Label(root, image = img2)
        panel2.image = img2 # keep a reference!
        panel2.pack()
        panel2.place(x=350,y=50)

         
        if u1 == rid:
            print("compared")
            #break
            status()
        else:
            print("rid="+str(rid))
            u1 += 1
            #test()
            
        print("u1="+str(u1))
        canvas.update()
        time.sleep(1)
        
        
    
def status():
    
    if f > 1:
        path = "upload/m1.jpg"
        
        messagebox.showinfo("Image","Image Uploaded Successfully")
        img = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
        
        panel = Label(root, image = img)
        panel.image = img # keep a reference!
        panel.pack()
        panel.place(x=50,y=50)

        b2 = Button(win2, text="Resize", command=resize)
        b2.pack()
        b2.place(x=190, y=650)
    else:
        messagebox.showinfo("Image","Incorrect Image!")
    
    
    
    
def resize():
    
    path = "upload/m1.jpg"
    mm = PIL.Image.open(path)
    mm = mm.resize((300,300), PIL.Image.ANTIALIAS)
    mm.save("upload/im1.jpg")
    path2 = "upload/im1.jpg"
    #messagebox.showinfo("Image","Image1 Uploaded Successfully")
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(path2))
    print("Resize")
    panel = Label(root, image = img)
    panel.image = img # keep a reference!
    panel.pack()
    panel.place(x=50,y=50)

def grayscale():
    
    print("Grayscale")
    path1 = "upload/im1.jpg"
    mm = PIL.Image.open(path1).convert('L')
    path = "upload/grayscale.jpg"
    mm.save("upload/grayscale.jpg")
    #messagebox.showinfo("Image","grayscale success")
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
    
    panel = Label(root, image = img)
    panel.image = img # keep a reference!
    panel.pack()
    panel.place(x=350,y=50)



def skeleton():
    path1 = "upload/grayscale.jpg"
    img = cv2.imread(path1,50)
    edges = cv2.Canny(img,50,70)
    #plt.subplot(121),plt.imshow(img,cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Feature'), plt.xticks([]), plt.yticks([])
    plt.savefig('upload/data.jpg')  
    #plt.show()
    path2 = 'upload/data.jpg'
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(path2))
    
    panel = Label(root, image = img)
    panel.image = img # keep a reference!
    panel.pack()
    panel.place(x=50,y=50)

def classi():
    print("rid==="+str(rid))
    print("Classification")
    password_provided = "xyz" # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

    input_file = 'test.encrypted'
    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)
    value=encrypted.decode("utf-8")
    dar=value.split('|')
    dv=dar[6]
    drw=dv.split('-')
    drn=int(drw[1])
    print(drw[0])
    print(drw[1])
    if drn<40:
        res = "Normal"
    elif drn<60:
        res = "Mild"
    else:
        res = "Severe"
    
      
    st="Glaucoma Level: "+res+" ("+drw[1]+"%)"
    a6 = Label(root, text='Classified Result: '+st)
    a6.pack()
    a6.place(x=50, y=500)





a1 = Label(root, text='Welcome',bg='lightyellow', fg='brown', font=("Helvetica", 16))
a1.pack()
a1.place(x=270, y=20)


ab1 = Button(root, text='Training', command=train)
ab1.pack()
ab1.place(x=250, y=50)

ab2 = Button(root, text='Testing', command=testing)
ab2.pack()
ab2.place(x=320, y=50)

'''b2 = Button(root, text="Resize", command=resize)
b2.pack()
b2.place(x=190, y=650)

b3 = Button(root, text="Grayscale", command=grayscale)
b3.pack()
b3.place(x=240, y=650)

b6 = Button(root, text="Classification", command=classi)
b6.pack()
b6.place(x=420, y=650)'''


root.configure(background='lightyellow')
root.title('Retina-Fundus Image-Glaucoma')
root.geometry("600x600")
