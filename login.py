import tkinter as tk
from tkinter import ttk, LEFT, END
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import cv2
import os

root = tk.Tk()
root.configure(background="black")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Login Form")

username = tk.StringVar()
password = tk.StringVar()

image2 = Image.open('img.jpg')
image2 = image2.resize((w, h), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0)

def shift():
    x1, y1, x2, y2 = canvas.bbox("marquee")
    if x2 < 0 or y1 < 0:
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height() // 2
        canvas.coords("marquee", x1, y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000 // fps, shift)

canvas = tk.Canvas(root, bg="#5499C7")
canvas.pack()
text_var = "Face Authentication"
text = canvas.create_text(0, -2000, text=text_var, font=('Algerian', 25, 'bold'), fill='white', tags=("marquee",), anchor='w')
x1, y1, x2, y2 = canvas.bbox("marquee")
width = 1600
height = 100
canvas['width'] = width
canvas['height'] = height
fps = 40
shift()

def registration():
    from subprocess import call
    call(["python", "registration.py"])
    root.destroy()

def login():
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        db = sqlite3.connect('evaluation.db')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS registration (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)")
        db.commit()
        find_entry = 'SELECT * FROM registration WHERE username = ? and password = ?'
        c.execute(find_entry, [(username.get()), (password.get())])
        result = c.fetchall()

def update_label(str_T):
    result_label = tk.Label(root, text=str_T, width=40, font=("bold", 25), bg='bisque2', fg='black')
    result_label.place(x=450, y=400)

def Test_database():
    flag = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 100)
    recognizer.read('trainingdata.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 8, minSize=(int(minW), int(minH)))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 50:
                id = id
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                cv2.putText(img, 'Number of Faces : ' + str(len(faces)), (40, 40), font, 1, (255, 0, 0), 2)
                update_label('Woww!!!!!....Authenticated User..')
                cam.release()
                cv2.destroyAllWindows()
                ms.showinfo('Success', 'You have successfully logged in')
                from subprocess import call
                call(['python', 'GUI_Master.py'])
            else:
                id = "unknown Person Identified"
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
                update_label('Ooops!!!!!....Unauthenticated User..')
        
        cv2.imshow('camera', img)
        if cv2.waitKey(1) == ord('Q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def window():
    root.destroy()

btn = tk.Button(root, text="face capture", bg="#A9CCE3", font=("", 20), fg="black", width=11, height=1, command=Test_database)
btn.place(x=600, y=250)

exit = tk.Button(root, text="Exit", command=window, width=15, height=1, font=('times', 15, 'bold'), bg="#A9CCE3", fg="black")
exit.place(x=600, y=350)

root.mainloop()
