from tkinter import *

def apply_background(frame):
    bg_img = PhotoImage(file="assets/images/images.jfif")
    bg_label = Label(frame, image=bg_img)
    bg_label.image = bg_img  # keep reference
    bg_label.place(relwidth=1, relheight=1)