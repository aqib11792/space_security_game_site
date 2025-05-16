import json
from tkinter import *
from PIL import Image, ImageTk
from game.levels import show_home

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
       relief="flat", command=try_login).grid(row=2, columnspan=2, pady=10)
    

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