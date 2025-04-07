import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "C:\\Attendance-Management-system-using-face-recognition\\haarcascade_frontalface_default.xml"
trainimagelabel_path = "C:\\Attendance-Management-system-using-face-recognition\\TrainingImageLabel\\Trainner.yml"
trainimage_path = "C:\\Attendance-Management-system-using-face-recognition\\TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "C:\\Attendance-Management-system-using-face-recognition\\Attendance"


# Create custom button class with hover effect
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = "#64FFDA"
        self["foreground"] = "#0A192F"

    def on_leave(self, e):
        self["background"] = self.defaultBackground
        self["foreground"] = self.defaultForeground


window = Tk()
window.title("Face Recognition Attendance System")
window.geometry("1280x720")
window.configure(background="#0A192F")  # Dark navy blue background
window.resizable(True, True)

# Center the window on screen
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x150")
    try:
        sc1.iconbitmap("AMS.ico")
    except:
        pass
    sc1.title("Warning!")
    sc1.configure(background="#0A192F")
    sc1.resizable(0, 0)
    
    # Center error window
    sc1.update_idletasks()
    width = sc1.winfo_width()
    height = sc1.winfo_height()
    x = (sc1.winfo_screenwidth() // 2) - (width // 2)
    y = (sc1.winfo_screenheight() // 2) - (height // 2)
    sc1.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    tk.Label(
        sc1,
        text="ID No & Name required!",
        fg="#64FFDA",
        bg="#0A192F",
        font=("Verdana", 16, "bold"),
    ).pack(pady=20)
    
    HoverButton(
        sc1,
        text="OK",
        command=del_sc1,
        fg="#64FFDA",
        bg="#172A45",
        width=9,
        height=1,
        activebackground="#64FFDA",
        activeforeground="#0A192F",
        relief=FLAT,
        font=("Verdana", 16, "bold"),
    ).pack(pady=10)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Create top header frame
header_frame = Frame(window, bg="#0A192F", pady=10)
header_frame.pack(fill=X)

# Logo and title in header frame
try:
    logo = Image.open("C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\0001.png")
    logo = logo.resize((60, 60), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(header_frame, image=logo1, bg="#0A192F")
    logo_label.pack(side=LEFT, padx=(450, 10))
except Exception as e:
    print(f"Error loading logo: {e}")

title_label = tk.Label(
    header_frame, text="Presence+", bg="#0A192F", fg="#64FFDA", font=("Verdana", 32, "bold"),
)
title_label.pack(side=LEFT)

# Welcome text
welcome_frame = Frame(window, bg="#0A192F", pady=20)
welcome_frame.pack(fill=X)

welcome_text = tk.Label(
    welcome_frame,
    text="Welcome to Presence+",
    bg="#0A192F",
    fg="#64FFDA",
    font=("Verdana", 36, "bold"),
)
welcome_text.pack()

subtitle = tk.Label(
    welcome_frame,
    text="Facial Recognition Attendance Management System",
    bg="#0A192F",
    fg="#8892B0",  # Light slate color for subtitle
    font=("Verdana", 16),
)
subtitle.pack(pady=10)

# Create content frame
content_frame = Frame(window, bg="#0A192F", pady=20)
content_frame.pack(fill=BOTH, expand=True)

# Image cards for options
card_frame = Frame(content_frame, bg="#0A192F")
card_frame.pack(pady=10)

# Function to create an option card
def create_card(parent, image_path, title, command, x_pos):
    card = Frame(parent, bg="#172A45", bd=0, highlightthickness=0, padx=20, pady=20, relief=FLAT)
    card.place(x=x_pos, y=150, width=250, height=300)
    
    try:
        img = Image.open(image_path)
        img = img.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = Label(card, image=photo, bg="#172A45")
        img_label.image = photo  # Keep a reference
        img_label.pack(pady=10)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
    
    title_label = Label(
        card, 
        text=title,
        bg="#172A45",
        fg="#64FFDA",
        font=("Verdana", 16, "bold")
    )
    title_label.pack(pady=10)
    
    btn = HoverButton(
        card,
        text=title,
        command=command,
        bg="#0A192F",
        fg="#64FFDA",
        font=("Verdana", 14),
        width=16,
        height=1,
        bd=0,
        relief=FLAT,
        activebackground="#64FFDA",
        activeforeground="#0A192F"
    )
    btn.pack(pady=10)
    
    return card

# Create cards for each option
try:
    register_card = create_card(
        content_frame, 
        "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\register.png",
        "Register", 
        TakeImageUI,
        150
    )
    
    attendance_card = create_card(
        content_frame, 
        "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\verifyy.png",
        "Mark Attendance", 
        automatic_attedance,
        500
    )
    
    view_card = create_card(
        content_frame, 
        "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\attendance.png",
        "View Attendance", 
        view_attendance,
        850
    )
except NameError:
    # Functions defined later in the file, so we'll create these after function definitions
    pass

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register New Student")
    ImageUI.geometry("780x550")
    ImageUI.configure(background="#0A192F")
    ImageUI.resizable(0, 0)
    
    # Center the window
    ImageUI.update_idletasks()
    width = ImageUI.winfo_width()
    height = ImageUI.winfo_height()
    x = (ImageUI.winfo_screenwidth() // 2) - (width // 2)
    y = (ImageUI.winfo_screenheight() // 2) - (height // 2)
    ImageUI.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    header_frame = Frame(ImageUI, bg="#0A192F", pady=10)
    header_frame.pack(fill=X)
    
    title_label = tk.Label(
        header_frame, text="Register Your Face", bg="#0A192F", fg="#64FFDA", font=("Verdana", 30, "bold"),
    )
    title_label.pack()

    subtitle = tk.Label(
        header_frame,
        text="Enter the details below",
        bg="#0A192F",
        fg="#8892B0",
        font=("Verdana", 16),
    )
    subtitle.pack(pady=10)
    
    # Create a container frame with elegant styling
    form_frame = Frame(ImageUI, bg="#172A45", bd=0, relief=FLAT, padx=40, pady=30)
    form_frame.pack(padx=50, pady=20, fill=X)

    # ID NO label
    id_frame = Frame(form_frame, bg="#172A45", pady=10)
    id_frame.pack(fill=X)
    
    lbl1 = tk.Label(
        id_frame,
        text="ID Number:",
        bg="#172A45",
        fg="#64FFDA",
        font=("Verdana", 14),
        anchor='w'
    )
    lbl1.pack(side=LEFT, padx=5)
    
    txt1 = tk.Entry(
        id_frame,
        width=25,
        bd=0,
        validate="key",
        bg="#0A192F",
        fg="#FFFFFF",
        relief=FLAT,
        highlightbackground="#64FFDA",
        highlightthickness=1,
        font=("Verdana", 15),
        insertbackground="#FFFFFF"
    )
    txt1.pack(side=LEFT, padx=10, ipady=8)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name
    name_frame = Frame(form_frame, bg="#172A45", pady=10)
    name_frame.pack(fill=X, pady=10)
    
    lbl2 = tk.Label(
        name_frame,
        text="Full Name:",
        bg="#172A45",
        fg="#64FFDA",
        font=("Verdana", 14),
        anchor='w'
    )
    lbl2.pack(side=LEFT, padx=5)
    
    txt2 = tk.Entry(
        name_frame,
        width=25,
        bd=0,
        bg="#0A192F",
        fg="#FFFFFF",
        relief=FLAT,
        highlightbackground="#64FFDA",
        highlightthickness=1,
        font=("Verdana", 15),
        insertbackground="#FFFFFF"
    )
    txt2.pack(side=LEFT, padx=10, ipady=8)

    # Notification area
    notification_frame = Frame(form_frame, bg="#172A45", pady=10)
    notification_frame.pack(fill=X, pady=10)
    
    lbl3 = tk.Label(
        notification_frame,
        text="Status:",
        bg="#172A45",
        fg="#64FFDA",
        font=("Verdana", 14),
        anchor='w'
    )
    lbl3.pack(side=LEFT, padx=5)
    
    message = tk.Label(
        notification_frame,
        text="",
        width=35,
        height=2,
        bd=0,
        bg="#0A192F",
        fg="#FFFFFF",
        relief=FLAT,
        font=("Verdana", 12),
        anchor='w',
        padx=10,
        highlightbackground="#64FFDA",
        highlightthickness=1
    )
    message.pack(side=LEFT, padx=10, fill=X, expand=True)

    # Buttons frame
    button_frame = Frame(form_frame, bg="#172A45", pady=15)
    button_frame.pack(fill=X)
    
    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    takeImg = HoverButton(
        button_frame,
        text="Take Image",
        command=take_image,
        bd=0,
        font=("Verdana", 14, "bold"),
        bg="#0A192F",
        fg="#64FFDA",
        height=2,
        width=12,
        relief=FLAT,
        activebackground="#64FFDA",
        activeforeground="#0A192F"
    )
    takeImg.pack(side=LEFT, padx=20, expand=True)

    trainImg = HoverButton(
        button_frame,
        text="Train Image",
        command=train_image,
        bd=0,
        font=("Verdana", 14, "bold"),
        bg="#0A192F",
        fg="#64FFDA",
        height=2,
        width=12,
        relief=FLAT,
        activebackground="#64FFDA",
        activeforeground="#0A192F"
    )
    trainImg.pack(side=LEFT, padx=20, expand=True)


# Create the cards after function definitions
register_card = create_card(
    content_frame, 
    "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\register.png",
    "Register", 
    TakeImageUI,
    150
)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

attendance_card = create_card(
    content_frame, 
    "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\verifyy.png",
    "Mark Attendance", 
    automatic_attedance,
    500
)

def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

view_card = create_card(
    content_frame, 
    "C:\\Attendance-Management-system-using-face-recognition\\UI_Image\\attendance.png",
    "View Attendance", 
    view_attendance,
    850
)

# Footer with exit button
footer_frame = Frame(window, bg="#0A192F", pady=20)
footer_frame.pack(side=BOTTOM, fill=X)

exit_btn = HoverButton(
    footer_frame,
    text="EXIT",
    command=quit,
    bd=0,
    font=("Verdana", 14, "bold"),
    bg="#172A45",
    fg="#64FFDA",
    width=10,
    height=1,
    relief=FLAT,
    activebackground="#64FFDA",
    activeforeground="#0A192F"
)
exit_btn.pack(pady=10)

# Add app info
version_label = Label(
    footer_frame,
    text="Version 1.0 • Facial Recognition Attendance System",
    bg="#0A192F",
    fg="#8892B0",
    font=("Verdana", 8)
)
version_label.pack(pady=5)

window.mainloop()
