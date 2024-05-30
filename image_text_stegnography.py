# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:15:05 2024

@author: COMPUTER
"""

import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time

#import tfModel_test as tf_test
global fn,img,img2,img3
global fn
global fn1
global fn2
global fn3

fn=""
##############################################+=============================================================
root = tk.Tk()
dt = tk.StringVar()
root.configure(background="seashell2")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Detection of information Hiding using image")


#430
#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('st.webp')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)
# #
lbl = tk.Label(root, text="Detection of information Hiding using barcode image and video ", font=('times', 35,' bold '), height=1, width=60,bg="#152238",fg="white")
lbl.place(x=0, y=0)

def shift():
    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): #reset the coordinates
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

canvas=tk.Canvas(root,bg="#152238")
canvas.pack()
canvas.place(x=0, y=0)
text_var="Detection of information Hiding using barcode image and video"
text=canvas.create_text(0,-2000,text=text_var,font=('Raleway',25,'bold'),fill='white',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = 1600
height = 80
canvas['width']=width
canvas['height']=height
fps=40    
shift()   






frame_alpr = tk.LabelFrame(root, text=" --Process-- ", width=220, height=550, bd=5, font=('times', 14, ' bold '),bg="#152238")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=20, y=100)


################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
import click
from PIL import Image


class Steganography:

    @staticmethod
    def __int_to_bin(rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple (e.g. (220, 110, 96))
        :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        """
        r, g, b = rgb
        return (f'{r:08b}',
                f'{g:08b}',
                f'{b:08b}')

    @staticmethod
    def __bin_to_int(rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :return: Return an int tuple (e.g. (220, 110, 96))
        """
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def __merge_rgb(rgb1, rgb2):
        """Merge two RGB tuples.

        :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
        :param rgb2: Another string tuple
        (e.g. ("00101010", "11101011", "00010110"))
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
    def merge(img1, img2):
        print(3)
        """Merge two images. The second one will be merged into the first one.

        :param img1: First image
        :param img2: Second image
        :return: A new merged image.
        """

        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.__int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.__merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        """Unmerge an image.

        :param img: The input image.
        :return: The unmerged/extracted image.
        """

        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image




#################################################################################################################
def window():
    root.destroy()

def uploadi():
    global fn
   
    fileNameu = askopenfilename(initialdir='/dataset', title='Select image for Aanalysis ',
                               filetypes=[("all files", "*.*")])
    IMAGE_SIZE=300
    imgpath = fileNameu
    fn = fileNameu
    img = Image.open(imgpath)
    
    img = img.resize((IMAGE_SIZE,200))
    img = np.array(img)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(img.shape[0])
    y1 = int(img.shape[1])



    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(im)
    img = tk.Label(root, image=imgtk, height=250, width=250)
    img.image = imgtk
    img.place(x=250, y=100)
    ms.showinfo("messege", "Input Image Uploaded sucessfully")
    
def hide1():
    global fn1
   
    fileName = askopenfilename(initialdir='/dataset', title='Select image for Aanalysis ',
                               filetypes=[("all files", "*.*")])
    IMAGE_SIZE=300
    imgpath1 = fileName
    fn1 = fileName
    img1 = Image.open(imgpath1)
    
    img1 = img1.resize((IMAGE_SIZE,200))
    img1 = np.array(img1)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(img1.shape[0])
    y1 = int(img1.shape[1])



    # im1 = Image.fromarray(img1)
    # imgtk1 = ImageTk.PhotoImage(im1)
    # img1 = tk.Label(root, image=imgtk1, height=250, width=250)
    # img1.image = imgtk1
    # img1.place(x=520, y=100)
    ms.showinfo("messege", "Hide 1 Image Uploaded sucessfully")

def hide2():
    global fn2
   
    fileName1 = askopenfilename(initialdir='/dataset', title='Select image for Aanalysis ',
                               filetypes=[("all files", "*.*")])
    IMAGE_SIZE=300
    imgpath2 = fileName1
    fn2 = fileName1
    img2 = Image.open(imgpath2)
    
    img2 = img2.resize((IMAGE_SIZE,200))
    img2 = np.array(img2)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(img2.shape[0])
    y1 = int(img2.shape[1])



    # im2 = Image.fromarray(img2)
    # imgtk2 = ImageTk.PhotoImage(im2)
    # img2 = tk.Label(root, image=imgtk2, height=250, width=250)
    # img2.image = imgtk2
    # img2.place(x=800, y=100)
    ms.showinfo("messege", "Hide 2 Image Uploaded sucessfully")
    
def hide3():
    global fn3
   
    fileName2 = askopenfilename(initialdir='/dataset', title='Select image for Aanalysis ',
                               filetypes=[("all files", "*.*")])
    IMAGE_SIZE=300
    imgpath3 = fileName2
    fn3 = fileName2
    img3 = Image.open(imgpath3)
    
    img3 = img3.resize((IMAGE_SIZE,200))
    img3 = np.array(img3)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(img3.shape[0])
    y1 = int(img3.shape[1])



    # im3 = Image.fromarray(img3)
    # imgtk3 = ImageTk.PhotoImage(im3)
    # img3 = tk.Label(root, image=imgtk3, height=250, width=250)
    # img3.image = imgtk3
    # img3.place(x=1050, y=100)
    ms.showinfo("messege", "Hide 3 Image Uploaded sucessfully")
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def decode1(image_name):
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    print(decoded_data)
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]
    
def sub():
    global fn
    global fn1
    global fn2
    global fn3
    imgn = fn
    print(imgn)
    imgn1 = fn1
    imgn2 = fn2
    imgn3 = fn3
    fna=dt.get()
    # text_img = ".\encoded_image.png"
    #img1 = text_img
    img2 = imgn1
    #this is the path where we will save the encoded Image.
    output = ".\encode.png"

    merged_image = Steganography.merge(Image.open(imgn), Image.open(imgn1))
    merged_image.save(output)
    print("encode 1")
    img3 = ".\encode.png"
    img4 = imgn2
    #this is the path where we will save the encoded Image.
    output1 = ".\encode1.png"

    merged_image = Steganography.merge(Image.open(img3), Image.open(img4))
    merged_image.save(output1)
    print("encode 2")
    img5 = ".\encode1.png"
    img6 = imgn3
    #this is the path where we will save the encoded Image.
    output2 = ".\encode2.png"

    merged_image = Steganography.merge(Image.open(img5), Image.open(img6))
    merged_image.save(output2)
    
    IMAGE_SIZE=200
    merged_image = merged_image.resize((IMAGE_SIZE,200))
    merged_image = np.array(merged_image)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(merged_image.shape[0])
    y1 = int(merged_image.shape[1])



    im = Image.fromarray(merged_image)
    imgtk = ImageTk.PhotoImage(im)
    img = tk.Label(root, image=imgtk, height=250, width=250)
    img.image = imgtk
    img.place(x=250, y=400)
    
    print(4)
    input_image = "encode2.png"
    output_image = "encoded_image.PNG"
    print(output_image)
    secret_data = fna
    print(secret_data)
    # encode the data into the image
    encoded_image = encode(image_name=input_image, secret_data=str(secret_data))
    # save the output image (encoded image)
    cv2.imwrite(output_image, encoded_image)
    
   
    
    
    
    print("encode 3")
def dec():
    
    output_image = "encoded_image.PNG"
    
    decoded_data = decode1(output_image)
    print("[+] Decoded data:", decoded_data)
    l6 = tk.Label(root, text=decoded_data, width=30, font=("Times new roman", 15, "bold"), bg="snow")
    l6.place(x=500, y=700)
    
    #img7 = ".\encode2.png"
    decode2 = ".\decode2.png"
    unmerged_image = Steganography.unmerge(Image.open(output_image))
    unmerged_image.save(decode2)
    
    IMAGE_SIZE=200
    i1=Image.open("decode2.png")
    print("file open")
    i1 = i1.resize((IMAGE_SIZE,200))
    i1 = np.array(i1)
    x1 = int(i1.shape[0])
    y1 = int(i1.shape[1])
    im1 = Image.fromarray(i1)
    imgtk1 = ImageTk.PhotoImage(im1)
    img1 = tk.Label(root, image=imgtk1, height=250, width=250)
    img1.image = imgtk1
    img1.place(x=550, y=400)
    print(5)
    
    img8 = ".\encode1.png"
    decode3 = ".\decode3.png"
    unmerged_image1 = Steganography.unmerge(Image.open(img8))
    unmerged_image1.save(decode3)
    IMAGE_SIZE=200
    i2=Image.open("decode3.png")
    i2 = i2.resize((IMAGE_SIZE,200))
    i2 = np.array(i2)
    x1 = int(i2.shape[0])
    y1 = int(i2.shape[1])
    im1 = Image.fromarray(i2)
    imgtk1 = ImageTk.PhotoImage(im1)
    img2 = tk.Label(root, image=imgtk1, height=250, width=250)
    img2.image = imgtk1
    img2.place(x=850, y=400)
    
    print(6)
    
    img9 = ".\encode.png"
    decode = ".\decode.png"
    unmerged_image2 = Steganography.unmerge(Image.open(img9))
    unmerged_image2.save(decode)
    IMAGE_SIZE=200
    i2=Image.open("decode.png")
    print(type(i2))
    
    i2 = i2.resize((IMAGE_SIZE,200))
    i2 = np.array(i2)
    x1 = int(i2.shape[0])
    y1 = int(i2.shape[1])
    im2 = Image.fromarray(i2)
    imgtk2 = ImageTk.PhotoImage(im2)
    img2 = tk.Label(root, image=imgtk2, height=250, width=250)
    img2.image = imgtk2
    img2.place(x=1060, y=400)
    
    print(5)
  
    
def home():
    from subprocess import call
    call(["python", "gui_main.py"])   

button1 = tk.Button(frame_alpr, text=" Upload Input Image ", command=uploadi,width=15, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
button1.place(x=10, y=50)

button2 = tk.Button(frame_alpr, text="Upload Hide Image", command=hide1, width=15, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
button2.place(x=10, y=100)

t4 = tk.Entry(frame_alpr, textvar=dt,show="*a", width=20, font=('', 15))
t4.place(x=0, y=150)

button3 = tk.Button(frame_alpr, text="Home", command=home, width=15, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
button3.place(x=10, y=400)
#
button4 = tk.Button(frame_alpr, text="Upload Hide 1 Image", command=hide2,width=15, height=1,bg="white",fg="black", font=('times', 15, ' bold '))
button4.place(x=10, y=200)
#

button5 = tk.Button(frame_alpr, text="Upload Hide 2 Image", command=hide3,width=15, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
button5.place(x=10, y=250)

button5 = tk.Button(frame_alpr, text="Encode", command=sub,width=15, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button5.place(x=10, y=300)

button5 = tk.Button(frame_alpr, text="Decode", command=dec,width=15, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button5.place(x=10, y=350)


exit = tk.Button(frame_alpr, text="Exit", command=window, width=15, height=1, font=('times', 15, ' bold '),bg="red",fg="white")
exit.place(x=10, y=450)



root.mainloop()