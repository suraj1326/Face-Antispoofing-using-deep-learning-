import tkinter as tk
# from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from tkinter import * 
import tkinter as tk
from tkinter import ttk, LEFT, END
import time
import numpy as np
import cv2
import os
from PIL import Image , ImageTk     
from PIL import Image # For face recognition we will the the LBPH Face Recognizer 
import pandas as pd
#import openpyxl
#import xlwrite,firebase.firebase_ini as fire
from tkinter import messagebox as ms

window = tk.Tk()
window.geometry("1600x800")
window.title("REGISTRATION FORM")
window.configure(background="grey")

Fullname = tk.StringVar()
address = tk.StringVar()
userid = tk.IntVar()
Email = tk.StringVar()
Phoneno = tk.IntVar()
var = tk.IntVar()
age = tk.IntVar()

image2 = Image.open('1.jpg')
image2 = image2.resize((1500,700), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(window, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)

# value = random.randint(1, 1000)
# print(value)

# database code
db = sqlite3.connect('evaluation.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS registration"
               "(Fullname TEXT, address TEXT, userid TEXT, Email TEXT, Phoneno TEXT,Gender TEXT,age TEXT )")
db.commit()





def insert():
    fname = Fullname.get()
    addr = address.get()
    un = userid.get()
    email = Email.get()
    mobile = Phoneno.get()
    gender = var.get()
    time = age.get()
    
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()

    # Find Existing username if any take proper action
    find_user = ('SELECT * FROM registration WHERE userid = ?')
    c.execute(find_user, [(userid.get())])

    # else:
    #   ms.showinfo('Success!', 'Account Created Successfully !')

    # to check mail
    #regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        a = True
    else:
        a = False
    # validation
    if (fname.isdigit() or (fname == "")):
        ms.showinfo("Message", "please enter valid name")
    elif (addr == ""):
        ms.showinfo("Message", "Please Enter Address")
    elif (email == "") or (a == False):
        ms.showinfo("Message", "Please Enter valid email")
    elif((len(str(mobile)))<10 or len(str((mobile)))>10):
        ms.showinfo("Message", "Please Enter 10 digit mobile number")
    elif ((time > 100) or (time == 0)):
        ms.showinfo("Message", "Please Enter valid age")
    elif (c.fetchall()):
        ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
    
        ms.showinfo("Message", "Please Enter gender")
    
    
    else:
        conn = sqlite3.connect('evaluation.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO registration(Fullname, address, userid, Email, Phoneno, Gender, age ) VALUES(?,?,?,?,?,?,?)',
                (fname, addr, un, email, mobile, gender, time))

            conn.commit()
            db.close()
            ms.showinfo('Success!', 'Account Created Successfully !')
            # window.destroy()
            window.destroy()
            
            Create_database()
            
           
            
            from subprocess import call
            call(["python", "login.py"])

def Train_database():
           
    recognizer =cv2.face.LBPHFaceRecognizer_create();
    
    path="facesData"
    
    def getImagesWithID(path):
    
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]   
    
     # print image_path   
    
     #getImagesWithID(path)
    
        faces = []
    
        IDs = []
    
        for imagePath in imagePaths:      
    
      # Read the image and convert to grayscale
    
            facesImg = Image.open(imagePath).convert('L')
    
            faceNP = np.array(facesImg, 'uint8')
    
            # Get the label of the image
            
    
            ID= int(os.path.split(imagePath)[-1].split(".")[1])
    
             # Detect the face in the image
    
            faces.append(faceNP)
    
            IDs.append(ID)
    
            cv2.imshow("Adding faces for traning",faceNP)
    
            cv2.waitKey(10)
    
        return np.array(IDs), faces
    
    Ids,faces  = getImagesWithID(path)
    
    recognizer.train(faces,Ids)
    
    recognizer.save("trainingdata.yml")
    
    cv2.destroyAllWindows()


########################################################################################################################
def Create_database():
        
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0)
    
#    id = input('enter user id')
    id=userid.get()
    
    sampleN=0;
    
    while 1:
    
        ret, img = cap.read()
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
        for (x,y,w,h) in faces:
    
            sampleN=sampleN+1;
    
            cv2.imwrite("facesData/User."+str(id)+ "." +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])
    
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
            cv2.waitKey(100)
    
        cv2.imshow('img',img)
    
        cv2.waitKey(1)
    
        if sampleN > 40:
    
            break
    
    cap.release()
    #entry2.delete(0,'end')
    cv2.destroyAllWindows()
    Train_database()
    





l1 = tk.Label(window, text="Registration Form", font=("Times new roman", 30, "bold"), bg="#2980B9", fg="white")
l1.place(x=610, y=50)

# that is for label1 registration

l2 = tk.Label(window, text="Full Name :", width=14, font=("Times new roman", 15), bg="#EAFAF1", fg="black")
l2.place(x=465, y=150)
t1 = tk.Entry(window, textvar=Fullname, width=35, font=('', 15))
t1.place(x=700, y=150)
# that is for label 2 (full name)


l3 = tk.Label(window, text="Address :", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l3.place(x=465, y=200)
t2 = tk.Entry(window, textvar=address, width=35, font=('', 15))
t2.place(x=700, y=200)
# that is for label 3(address)


# that is for label 4(blood group)

l5 = tk.Label(window, text="E-mail :", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l5.place(x=465, y=250)
t4 = tk.Entry(window, textvar=Email, width=35, font=('', 15))
t4.place(x=700, y=250)
# that is for email address

l6 = tk.Label(window, text="Phone number :", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l6.place(x=465, y=300)
t5 = tk.Entry(window, textvar=Phoneno, width=35, font=('', 15))
t5.place(x=700, y=300)
# phone number
l7 = tk.Label(window, text="Gender :", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l7.place(x=465, y=350)
# gender
tk.Radiobutton(window, text="Male", padx=5, width=10, bg="#EAFAF1", font=("bold", 15), variable=var, value=1).place(x=700,
                                                                                                                y=350)
tk.Radiobutton(window, text="Female", padx=20, width=12, bg="#EAFAF1", font=("bold", 15), variable=var, value=2).place(
    x=880, y=350)

l8 = tk.Label(window, text="Age :", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l8.place(x=465, y=400)
t6 = tk.Entry(window, textvar=age, width=35, font=('', 15))
t6.place(x=700, y=400)

l4 = tk.Label(window, text="User ID:", width=14, font=("Times new roman", 15, "bold"), bg="#EAFAF1", fg="black")
l4.place(x=465, y=450)
t3 = tk.Entry(window, textvar=userid, width=35, font=('', 15))
t3.place(x=700, y=450)




# btn = tk.Button(window, text="face capture", bg="#8B0A50",font=("",20),fg="white", width=9, height=1, command=Create_database)
# btn.place(x=700, y=650)
btn = tk.Button(window, text="SUBMIT", bg="#2980B9",font=("",20),fg="white", width=9, height=1, command=insert)
btn.place(x=700, y=600)
# tologin=tk.Button(window , text="Go To Login", bg ="dark green", fg = "white", width=15, height=2, command=login)
# tologin.place(x=330, y=600)
window.mainloop()