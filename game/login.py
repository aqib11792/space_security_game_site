import json
from tkinter import *
from PIL import Image, ImageTk
from game.levels import show_home

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def login_screen(root):
    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_img = ImageTk.PhotoImage(bg)

    bg_label = Label(root, image=bg_img)
    bg_label.image = bg_img
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(root, bg="white", padx=30, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame, text="Username", bg="white").grid(row=0, column=0)
    Label(frame, text="Password", bg="white").grid(row=1, column=0)

    uname = Entry(frame)
    pwd = Entry(frame, show="*")
    uname.grid(row=0, column=1)
    pwd.grid(row=1, column=1)

    def try_login():
        users = load_users()
        user = uname.get()
        pw = pwd.get()
        if user in users and users[user]["password"] == pw:
            root.destroy()
            show_home(user)
        else:
            Label(frame, text="Login Failed", fg="red", bg="white").grid(row=3, columnspan=2)

    Button(frame, text="Login", command=try_login).grid(row=2, columnspan=2, pady=10)
