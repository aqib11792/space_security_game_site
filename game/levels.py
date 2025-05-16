import json, random
import tkinter as tk
from PIL import Image, ImageTk
from game.game_engine import load_progress, save_progress
from game.sound import play_correct, play_wrong


class GameLevels:
    def __init__(self, username, start_from=None):
        self.username = username
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title("Game")
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        tk.Button(self.root, text="Logout", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
          command=self.logout).place(relx=0.01, rely=0.0, anchor="nw", x=10, y=10)

        self.bg_img = Image.open("assets/images/bg.jpg")
        self.bg_img = self.bg_img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        
        self.frame = tk.Frame(
            self.canvas,
            bg="#2b2e39",
            padx=40, pady=40,
            highlightbackground="#ffffff",
            highlightthickness=1,
            highlightcolor="#ffffff"
        )

        self.canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() // 2,
            window=self.frame,
            width=800,
            height=500
        )

        state = load_progress(username)
        self.score = state["score"]
        self.level = start_from if start_from else state["level"]
        self.q_index = 0
        self.questions = []
        self.wrong_attempts = 0

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 14, "bold"), bg="#1c1f26", fg="#00c3ff")
        self.score_label.place(relx=1.0, rely=0.0, anchor="ne", x=-40, y=10)

        self.run_current_level()
        self.root.mainloop()

    def logout(self):
        save_progress(self.username, {"score": self.score, "level": self.level})
        self.root.destroy()
        from game.login import user_login_screen
        new_root = tk.Tk()
        new_root.attributes('-fullscreen', True)
        user_login_screen(new_root)

    def run_current_level(self):
        if self.level > 5:
            self.show_final()
            return
        self.questions = self.load_level_questions(self.level)
        self.q_index = 0
        self.wrong_attempts = 0
        self.show_question()

    def show_question(self):
        if self.q_index >= len(self.questions):
            self.level += 1
            save_progress(self.username, {"score": self.score, "level": self.level})
            self.run_current_level()
            return

        self.clear_frame()
        question = self.questions[self.q_index]

        tk.Label(self.frame, text=f"Level {self.level} - Q{self.q_index + 1}", font=("Helvetica", 16, "bold"), bg="#2b2e39", fg="#ffffff").pack(pady=10)
        tk.Label(self.frame, text=question["question"], font=("Helvetica", 14), bg="#2b2e39", fg="#ffffff", wraplength=700).pack(pady=10)

        self.choice = tk.StringVar(value="")

        for k, v in question["options"].items():
            tk.Radiobutton(self.frame, text=f"{k}) {v}", variable=self.choice, value=k,
                           font=("Helvetica", 12), bg="#2b2e39", fg="#ffffff", selectcolor="#1c1f26",
                           activebackground="#2b2e39", activeforeground="#00c3ff").pack(anchor="w", padx=10)

        btns = tk.Frame(self.frame, bg="#2b2e39")
        btns.pack(pady=20)
        tk.Button(btns, text="Submit", command=lambda: self.check_answer(question), font=("Helvetica", 12), bg="#00c3ff", fg="#000000", relief="flat").grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Quit", command=self.goto_level_select, font=("Helvetica", 12), bg="#00c3ff", fg="#000000", relief="flat").grid(row=0, column=1, padx=10)

    def check_answer(self, question):
        if not self.choice.get():
            return
        selected = self.choice.get()
        if selected == question["answer"]:
            self.score += 10
            self.wrong_attempts = 0
            play_correct()
            self.q_index += 1
            self.update_score_display()
            self.show_question()
        else:
            self.score -= 5
            self.wrong_attempts += 1
            play_wrong()
            self.update_score_display()
            if self.score < 0 or self.wrong_attempts >= 3:
                self.try_again_screen()
            else:
                self.show_question()

    def try_again_screen(self):
        self.clear_frame()
        save_progress(self.username, {"score": self.score, "level": self.level})
        self.wrong_attempts = 0
        tk.Label(self.frame, text="❌ Too many wrong attempts!", font=("Helvetica", 16, "bold"), bg="#2b2e39", fg="red").pack(pady=10)
        tk.Button(self.frame, text="Back to Level Select", font=("Helvetica", 14), bg="#00c3ff", fg="#000000", relief="flat", command=self.goto_level_select).pack(pady=20)

    def goto_level_select(self):
        self.root.destroy()
        show_level_select(self.username)

    def quit_game(self):
        save_progress(self.username, {"score": self.score, "level": self.level})
        self.root.destroy()

    def show_final(self):
        self.clear_frame()
        save_progress(self.username, {"score": self.score, "level": self.level})
        tk.Label(self.frame, text="🎉 CONGRATULATIONS!", font=("Helvetica", 18, "bold"), bg="#2b2e39", fg="green").pack(pady=10)
        tk.Label(self.frame, text=f"You completed all 5 levels!\nFinal Score: {self.score}", font=("Helvetica", 14), bg="#2b2e39", fg="#ffffff").pack(pady=10)
        btns = tk.Frame(self.frame, bg="#2b2e39")
        btns.pack(pady=20)
        tk.Button(btns, text="Replay Game", font=("Helvetica", 12), command=self.reset_game, bg="#00c3ff", fg="#000000", relief="flat").grid(row=0, column=0, padx=10)
        tk.Button(btns, text="Back to Home", font=("Helvetica", 12), command=self.back_to_home, bg="#00c3ff", fg="#000000", relief="flat").grid(row=0, column=1, padx=10)
        tk.Button(btns, text="Quit", font=("Helvetica", 12), command=self.root.destroy, bg="#00c3ff", fg="#000000", relief="flat").grid(row=0, column=2, padx=10)
        
    def reset_game(self):
        save_progress(self.username, {"score": 0, "level": 1})
        self.root.destroy()
        show_level_select(self.username)

    def back_to_home(self):
        self.root.destroy()
        show_home(self.username)

    def update_score_display(self):
        self.score_label.config(text=f"Score: {self.score}")

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def load_level_questions(self, level):
        with open(f"data/level{level}_questions.json") as f:
            return random.sample(json.load(f), 2)


def show_home(username):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=bg, anchor="nw")

    frame = tk.Frame(canvas, bg="#2b2e39", padx=60, pady=60)
    canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, window=frame)

    tk.Label(frame, text="🌌 Welcome to Space Cyber Mission!\nYou are the commander of a security mission.\nSolve challenges to secure the galaxy.", 
             font=("Helvetica", 14), bg="#2b2e39", fg="#ffffff", wraplength=500, justify="center").pack(pady=(0, 20))

    tk.Button(frame, text="Start Game", bg="#00c3ff", fg="#000000", font=("Helvetica", 12), relief="flat",
              command=lambda: start_game(root, username)).pack(pady=10)

    # Lazy import to avoid circular import
    # Lazy import to avoid circular import
    def go_logout():
        root.destroy()
        from game.login import user_login_screen
        new_root = tk.Tk()
        new_root.attributes('-fullscreen', True)
        user_login_screen(new_root)  # ✅ Only call this once with fullscreen root

    tk.Button(root, text="Logout", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
            command=go_logout).place(relx=0.01, rely=0.0, anchor="nw", x=10, y=10)

    root.mainloop()



def start_game(window, username):
    window.destroy()
    show_level_select(username)


def show_level_select(username):
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Level Selection")
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    bg = Image.open("assets/images/bg.jpg")
    bg = bg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=bg, anchor="nw")

    frame = tk.Frame(canvas, bg="#2b2e39", padx=30, pady=30)
    canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, window=frame)

    progress = load_progress(username)
    unlocked_level = progress.get("level", 1)
    final_score = progress.get("score", 0)

    # Lock all levels except level 1 if score < 0
    if final_score < 0:
        final_score = 0
        unlocked_level = 1
        save_progress(username, {"score": 0, "level": 1})

    # Top left score label
    score_label = tk.Label(root, text=f"Score: {final_score}", font=("Helvetica", 14, "bold"),
                       bg="#1c1f26", fg="#00c3ff")
    score_label.place(relx=0.0, rely=0.0, anchor="nw", x=20, y=10)


    tk.Label(frame, text="Select Level", font=("Helvetica", 18), bg="#2b2e39", fg="#ffffff").pack(pady=10)

    def launch_level(level):
        root.destroy()
        GameLevels(username, start_from=level)

    # Generate level buttons
    for i in range(1, 6):
        if unlocked_level > 5 or i < unlocked_level:
            btn = tk.Button(frame, text=f"Level {i} ✅", font=("Helvetica", 14), state="disabled")  # completed levels
        elif i == unlocked_level:
            btn = tk.Button(frame, text=f"Level {i}", font=("Helvetica", 14), command=lambda l=i: launch_level(l))  # current level
        else:
            btn = tk.Button(frame, text=f"Level {i} 🔒", font=("Helvetica", 14), state="disabled")  # locked future levels
        btn.pack(pady=5)

    # FINAL LEVEL COMPLETED UI (clean, no duplicate buttons)
    if unlocked_level > 5:
        tk.Label(frame, text="🎉 All Levels Completed!", font=("Helvetica", 14), bg="white", fg="green").pack(pady=10)
        tk.Button(frame, text="View Final Score", font=("Helvetica", 12),
          command=lambda: show_final_score_popup(root, final_score)).pack(pady=5)
        tk.Button(frame, text="Replay Game", font=("Helvetica", 12),
                  command=lambda: reset_progress(root, username)).pack(pady=5)

    tk.Button(frame, text="✖ Quit", font=("Helvetica", 12), command=root.destroy).pack(pady=20)
    def logout_to_login():
        root.destroy()
        from game.login import user_login_screen
        new_root = tk.Tk()
        new_root.attributes('-fullscreen', True)
        user_login_screen(new_root)

    tk.Button(root, text="Logout", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
            command=logout_to_login).place(relx=0.01, rely=0.0, anchor="nw", x=10, y=10)


    root.mainloop()


def show_final_score_popup(window, score):
    popup = tk.Toplevel(window)
    popup.title("Final Score")
    popup.geometry("400x200")
    popup.resizable(False, False)
    popup.grab_set()

    tk.Label(popup, text="🎯 Final Score", font=("Helvetica", 16, "bold")).pack(pady=15)
    tk.Label(popup, text=f"Your final score is: {score}", font=("Helvetica", 14)).pack(pady=10)
    tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy).pack(pady=20)

def level_completed_popup(window, level, score):
    popup = tk.Toplevel(window)
    popup.title(f"Level {level} Completed")
    popup.geometry("400x200")
    tk.Label(popup, text=f"Level {level} is already completed!", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(popup, text=f"Your current score: {score}", font=("Helvetica", 12)).pack(pady=10)
    tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy).pack(pady=20)

def reset_progress(window, username):
    save_progress(username, {"score": 0, "level": 1})
    window.destroy()
    show_level_select(username)
