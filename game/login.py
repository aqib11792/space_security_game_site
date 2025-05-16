import json
from tkinter import *
from PIL import Image, ImageTk
from game.levels import show_home
import os
from tkinter import messagebox

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def go_back_to_main(window):
    window.destroy()
    launch_main_login()


def user_login_screen(root):
    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_img = ImageTk.PhotoImage(bg)

    bg_label = Label(root, image=bg_img)
    bg_label.image = bg_img
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    Button(root, text="← Back", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
       command=lambda: go_back_to_main(root)).place(relx=0.01, rely=0.01, anchor="nw")


    frame = Frame(root, bg="#2b2e39", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame, text="Username", bg="#2b2e39", fg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0)
    Label(frame, text="Password", bg="#2b2e39", fg="#ffffff", font=("Helvetica", 12)).grid(row=1, column=0)

    uname = Entry(frame, bg="#1c1f26", fg="#ffffff", insertbackground="#ffffff", width=25)
    pwd = Entry(frame, show="*", bg="#1c1f26", fg="#ffffff", insertbackground="#ffffff", width=25)
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

    Button(frame, text="Login", bg="#00c3ff", fg="#000000", font=("Helvetica", 12),
        relief="flat", command=try_login).grid(row=2, columnspan=2, pady=(10, 5))

    # Register button
    Button(frame, text="Register New User", bg="#00c3ff", fg="#000000", font=("Helvetica", 12),
        relief="flat", command=lambda: open_register_window(root)).grid(row=3, columnspan=2)

def open_register_window(old_root):
    old_root.destroy()
    register_root = Tk()
    register_root.attributes('-fullscreen', True)
    show_register_screen(register_root)

def show_register_screen(root):
    root.destroy()  # destroy the small login window

    root = Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="#1c1f26")

    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_img = ImageTk.PhotoImage(bg)
    Label(root, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
    root.bg_img = bg_img  # keep reference

    frame = Frame(root, bg="#2b2e39", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame, text="Register", font=("Helvetica", 16, "bold"), bg="#2b2e39", fg="white").grid(row=0, columnspan=2, pady=10)

    Label(frame, text="Username", bg="#2b2e39", fg="white").grid(row=1, column=0, sticky="e")
    username = Entry(frame, bg="#1c1f26", fg="white", insertbackground="white")
    username.grid(row=1, column=1)

    Label(frame, text="Password", bg="#2b2e39", fg="white").grid(row=2, column=0, sticky="e")
    password = Entry(frame, show="*", bg="#1c1f26", fg="white", insertbackground="white")
    password.grid(row=2, column=1)

    Label(frame, text="Re-enter Password", bg="#2b2e39", fg="white").grid(row=3, column=0, sticky="e")
    re_password = Entry(frame, show="*", bg="#1c1f26", fg="white", insertbackground="white")
    re_password.grid(row=3, column=1)

    msg_label = Label(frame, text="", bg="#2b2e39", fg="red")
    msg_label.grid(row=4, columnspan=2)

    def register_user():
        user = username.get().strip()
        pw = password.get()
        re_pw = re_password.get()

        if not user or not pw or not re_pw:
            msg_label.config(text="All fields are required!", fg="red")
            return

        if pw != re_pw:
            msg_label.config(text="Passwords do not match!", fg="red")
            return

        users_path = "data/users.json"
        progress_path = "data/progress.json"

        if not os.path.exists(users_path):
            json.dump({}, open(users_path, "w"))
        if not os.path.exists(progress_path):
            json.dump({}, open(progress_path, "w"))

        with open(users_path, "r") as f:
            users = json.load(f)

        if user in users:
            msg_label.config(text="Username already exists!", fg="red")
            return

        users[user] = {"password": pw, "role": "player"}
        with open(users_path, "w") as f:
            json.dump(users, f, indent=2)

        with open(progress_path, "r") as f:
            progress = json.load(f)
        progress[user] = {"score": 0, "level": 1}
        with open(progress_path, "w") as f:
            json.dump(progress, f, indent=2)

        msg_label.config(text="✅ Registration successful! Redirecting...", fg="green")
        print("Registration successful for user:", user)

        root.after(1500, lambda: [root.destroy(), user_login_screen(TkFull())])

    Button(frame, text="Register", bg="#00c3ff", fg="black", font=("Helvetica", 12),
           command=register_user).grid(row=5, columnspan=2, pady=10)

    Button(frame, text="Go Back", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
           command=lambda: go_back_to_login(root)).grid(row=6, columnspan=2)

def TkFull():
    win = Tk()
    win.attributes('-fullscreen', True)
    return win

def go_back_to_login(current_root):
    current_root.destroy()
    user_login_screen(TkFull())

def login_screen(root):
    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_img = ImageTk.PhotoImage(bg)

    bg_label = Label(root, image=bg_img)
    bg_label.image = bg_img
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(root, bg="#2b2e39", padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame, text="Select Login Type", font=("Helvetica", 16, "bold"),
          bg="#2b2e39", fg="white").pack(pady=20)

    Button(frame, text="User Login", bg="#00c3ff", fg="#000000", font=("Helvetica", 14),
           width=15, relief="flat", command=lambda: load_user_login(root))\
           .pack(pady=10)

    Button(frame, text="Admin Login", bg="#00c3ff", fg="#000000", font=("Helvetica", 14),
           width=15, relief="flat", command=lambda: load_admin_login(root))\
           .pack(pady=10)


def load_user_login(window):
    window.destroy()
    root = Tk()
    root.attributes('-fullscreen', True)
    user_login_screen(root)
    root.mainloop()

def load_admin_login(window):
    window.destroy()
    import admin.admin_console as admin_console
    admin_console.admin_login_screen()

def launch_main_login():
    root = Tk()
    root.attributes("-fullscreen", True)
    login_screen(root)
    root.mainloop()