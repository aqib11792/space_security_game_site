import json
import tkinter as tk
from tkinter import ttk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

USERS_FILE = os.path.join(DATA_DIR, "users.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")


class AdminConsole:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#2b2e39")

        tk.Label(self.root, text="Admin Login", font=("Helvetica", 16), bg="#2b2e39", fg="white").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#2b2e39", fg="white").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg="#2b2e39", fg="white").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.error_label = tk.Label(self.root, text="", fg="red", bg="#2b2e39")
        self.error_label.pack()

        tk.Button(self.root, text="Login", command=self.login, bg="#00c3ff", fg="black").pack(pady=20)

        self.root.mainloop()

    def login(self):
        user = self.username_entry.get()
        pw = self.password_entry.get()
        if user == "admin" and pw == "admin123":
            self.root.destroy()
            AdminPanel()
        else:
            self.error_label.config(text="Invalid admin credentials")


class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Console")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1c1f26")
        tk.Button(self.root, text="Logout", command=self.logout, bg="#ff4d4d", fg="white")\
            .place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        tk.Button(self.root, text="Logout", bg="#ff4d4d", fg="white", font=("Helvetica", 10),
          command=self.logout).place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
    
        self.manage_users_tab(notebook)
        self.manage_question_tab(notebook)
        self.manage_progress_tab(notebook)

        self.root.mainloop()
    
    def logout(self):
        self.root.destroy()
        AdminConsole()

    def manage_users_tab(self, notebook):
        frame = tk.Frame(notebook, bg="#2b2e39")
        notebook.add(frame, text="User Management")

        tk.Label(frame, text="Username", bg="#2b2e39", fg="white").grid(row=0, column=0)
        self.username_input = tk.Entry(frame)
        self.username_input.grid(row=0, column=1)

        self.user_msg = tk.Label(frame, text="", bg="#2b2e39", fg="white")
        self.user_msg.grid(row=1, columnspan=3)

        tk.Button(frame, text="Search", command=self.search_user, bg="#00c3ff").grid(row=0, column=2, padx=10)

        self.pw_label = tk.Label(frame, text="Password", bg="#2b2e39", fg="white")
        self.password_input = tk.Entry(frame)
        
        self.role_label = tk.Label(frame, text="Role", bg="#2b2e39", fg="white")
        self.role_var = tk.StringVar(value="player")
        self.role_dropdown = ttk.Combobox(frame, textvariable=self.role_var, values=["player", "admin"], state="readonly")

        self.action_button = tk.Button(frame)
        tk.Button(frame, text="Clear", command=self.clear_user_fields, bg="#444", fg="white").grid(row=5, column=0, columnspan=3, pady=5)

        self.user_frame = frame

    def search_user(self):
        user = self.username_input.get()
        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        self.pw_label.grid_forget()
        self.password_input.grid_forget()
        self.action_button.grid_forget()

        if user in users:
            self.user_msg.config(text="User exists. You can delete them.", fg="white")
            self.action_button = tk.Button(self.user_frame, text="Delete User", bg="red", fg="white", command=self.delete_user)
        else:
            self.user_msg.config(text="User not found. You can add them.", fg="white")
            self.pw_label.grid(row=2, column=0)
            self.password_input.grid(row=2, column=1)
            self.role_label.grid(row=3, column=0)
            self.role_dropdown.grid(row=3, column=1)
            self.action_button = tk.Button(self.user_frame, text="Add User", bg="#00c3ff", command=self.add_user)

        self.action_button.grid(row=4, column=0, columnspan=3, pady=10)

    def clear_user_fields(self):
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)
        self.user_msg.config(text="")
        self.pw_label.grid_forget()
        self.password_input.grid_forget()
        self.action_button.grid_forget()
        self.role_label.grid_forget()
        self.role_dropdown.grid_forget()
        self.pw_label.grid_forget()
        self.password_input.grid_forget()
        self.role_label.grid_forget()
        self.role_dropdown.grid_forget()
        self.action_button.grid_forget()
        self.role_var.set("player")


    def delete_user(self):
        user = self.username_input.get()
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        if user in users:
            del users[user]
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=2)

        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)
        if user in progress:
            del progress[user]
            with open(PROGRESS_FILE, "w") as f:
                json.dump(progress, f, indent=2)

        self.user_msg.config(text="User deleted", fg="green")

    def add_user(self):
        user = self.username_input.get()
        pwd = self.password_input.get()

        if not pwd:
            self.user_msg.config(text="Password required", fg="red")
            return

        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        if user in users:
            self.user_msg.config(text="User already exists", fg="red")
            return

        role = self.role_var.get()
        users[user] = {"password": pwd, "role": role}

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

        # ✅ Only add to progress if role is 'player'
        if role == "player":
            with open(PROGRESS_FILE, "r") as f:
                progress = json.load(f)
            progress[user] = {"score": 0, "level": 1}
            with open(PROGRESS_FILE, "w") as f:
                json.dump(progress, f, indent=2)

        self.user_msg.config(text="User added", fg="green")


    def manage_progress_tab(self, notebook):
        frame = tk.Frame(notebook, bg="#2b2e39")
        notebook.add(frame, text="Progress Management")

        tk.Label(frame, text="Username", bg="#2b2e39", fg="white").grid(row=0, column=0)
        self.user_entry = tk.Entry(frame)
        self.user_entry.grid(row=0, column=1)

        tk.Button(frame, text="Load Progress", command=self.load_progress, bg="#00c3ff").grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Score", bg="#2b2e39", fg="white").grid(row=2, column=0)
        self.score_entry = tk.Entry(frame)
        self.score_entry.grid(row=2, column=1)

        tk.Label(frame, text="Level", bg="#2b2e39", fg="white").grid(row=3, column=0)
        self.level_entry = tk.Entry(frame)
        self.level_entry.grid(row=3, column=1)

        self.progress_msg = tk.Label(frame, text="", bg="#2b2e39", fg="white")
        self.progress_msg.grid(row=4, column=0, columnspan=2)

        tk.Button(frame, text="Save Changes", command=self.save_progress, bg="green", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    def load_progress(self):
        user = self.user_entry.get()
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        if user in data:
            self.score_entry.delete(0, tk.END)
            self.level_entry.delete(0, tk.END)
            self.score_entry.insert(0, data[user]["score"])
            self.level_entry.insert(0, data[user]["level"])
            self.progress_msg.config(text="Progress loaded", fg="green")
        else:
            self.score_entry.delete(0, tk.END)
            self.level_entry.delete(0, tk.END)
            self.progress_msg.config(text="User not found", fg="red")

    def save_progress(self):
        user = self.user_entry.get()
        try:
            score = int(self.score_entry.get())
            level = int(self.level_entry.get())
            if score < 0:
                self.progress_msg.config(text="Score can't be < 0", fg="red")
                return
            if level < 1 or level > 5:
                self.progress_msg.config(text="Level must be 1-5", fg="red")
                return
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
            data[user] = {"score": score, "level": level}
            with open(PROGRESS_FILE, "w") as f:
                json.dump(data, f, indent=2)
            self.progress_msg.config(text="Progress updated", fg="green")
        except:
            self.progress_msg.config(text="Invalid input", fg="red")

    def manage_question_tab(self, notebook):
        self.qtab = tk.Frame(notebook, bg="#2b2e39")
        notebook.add(self.qtab, text="Question Management")
        self.render_question_mode()

    def render_question_mode(self):
        for w in self.qtab.winfo_children(): w.destroy()

        tk.Label(self.qtab, text="Choose Question Operation", font=("Helvetica", 16, "bold"),
                 bg="#2b2e39", fg="white").pack(pady=20)

        tk.Button(self.qtab, text="➕ Add New Question", command=self.render_add_question,
                  bg="#00c3ff", font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self.qtab, text="✏️ Edit/Delete Questions", command=self.render_edit_delete,
                  bg="#00c3ff", font=("Helvetica", 12)).pack(pady=10)

    def render_add_question(self):
        self.render_clear_qtab()

        tk.Label(self.qtab, text="Add New Question", font=("Helvetica", 16), bg="#2b2e39", fg="white").pack()

        self.level_var = tk.StringVar(value="1")
        levels = ttk.Combobox(self.qtab, textvariable=self.level_var, values=[str(i) for i in range(1, 6)])
        levels.pack()

        self.q_entry = tk.Entry(self.qtab, width=70)
        self.q_entry.pack()

        self.options = {}
        for k in ["A", "B", "C", "D"]:
            tk.Label(self.qtab, text=f"{k}:", bg="#2b2e39", fg="white").pack()
            self.options[k] = tk.Entry(self.qtab, width=50)
            self.options[k].pack()

        tk.Label(self.qtab, text="Correct Option", bg="#2b2e39", fg="white").pack()
        self.correct_option = tk.Entry(self.qtab)
        self.correct_option.pack()

        self.q_msg = tk.Label(self.qtab, text="", bg="#2b2e39", fg="white")
        self.q_msg.pack()

        tk.Button(self.qtab, text="Submit", command=self.add_question, bg="#00c3ff").pack(pady=5)
        tk.Button(self.qtab, text="🔙 Back", command=self.render_question_mode, bg="#444", fg="white").pack(pady=5)

    def add_question(self):
        level = self.level_var.get()
        question = self.q_entry.get()
        correct = self.correct_option.get().upper()
        options = {k: self.options[k].get() for k in self.options}
        if correct not in options:
            self.q_msg.config(text="Invalid correct option", fg="red")
            return
        data = {"question": question, "options": options, "answer": correct}
        file = os.path.join(DATA_DIR, f"level{level}_questions.json")
        try:
            with open(file, "r") as f:
                qdata = json.load(f)
        except:
            qdata = []
        qdata.append(data)
        with open(file, "w") as f:
            json.dump(qdata, f, indent=2)
        self.q_msg.config(text="Question added!", fg="green")

    def render_edit_delete(self):
        self.render_clear_qtab()

        tk.Label(self.qtab, text="Edit/Delete Questions", font=("Helvetica", 16), bg="#2b2e39", fg="white").pack()

        self.edit_level_var = tk.StringVar(value="1")
        levels = ttk.Combobox(self.qtab, textvariable=self.edit_level_var, values=[str(i) for i in range(1, 6)])
        levels.pack()
        levels.bind("<<ComboboxSelected>>", lambda e: self.load_questions_list())

        self.q_listbox = tk.Listbox(self.qtab, width=80)
        self.q_listbox.pack(pady=10)
        self.q_listbox.bind("<<ListboxSelect>>", self.populate_question_fields)

        self.edit_q_text = tk.Entry(self.qtab, width=70)
        self.edit_q_text.pack()

        self.edit_options = {}
        for k in ["A", "B", "C", "D"]:
            tk.Label(self.qtab, text=f"{k}:", bg="#2b2e39", fg="white").pack()
            self.edit_options[k] = tk.Entry(self.qtab, width=50)
            self.edit_options[k].pack()

        tk.Label(self.qtab, text="Correct Option", bg="#2b2e39", fg="white").pack()
        self.edit_correct = tk.Entry(self.qtab)
        self.edit_correct.pack()

        self.edit_msg = tk.Label(self.qtab, text="", bg="#2b2e39", fg="white")
        self.edit_msg.pack()

        tk.Button(self.qtab, text="Update", command=self.update_question, bg="green").pack()
        tk.Button(self.qtab, text="Delete", command=self.delete_question, bg="red").pack()
        tk.Button(self.qtab, text="🔙 Back", command=self.render_question_mode, bg="#444", fg="white").pack(pady=5)

    def load_questions_list(self):
        level = self.edit_level_var.get()
        file = os.path.join(DATA_DIR, f"level{level}_questions.json")
        self.q_listbox.delete(0, tk.END)
        try:
            with open(file, "r") as f:
                self.q_data = json.load(f)
            for idx, q in enumerate(self.q_data):
                self.q_listbox.insert(tk.END, f"{idx+1}: {q['question'][:60]}")
        except:
            self.edit_msg.config(text="Error loading questions", fg="red")

    def populate_question_fields(self, event):
        idx = self.q_listbox.curselection()
        if not idx: return
        q = self.q_data[idx[0]]
        self.edit_q_text.delete(0, tk.END)
        self.edit_q_text.insert(0, q["question"])
        for k in ["A", "B", "C", "D"]:
            self.edit_options[k].delete(0, tk.END)
            self.edit_options[k].insert(0, q["options"].get(k, ""))
        self.edit_correct.delete(0, tk.END)
        self.edit_correct.insert(0, q["answer"])

    def update_question(self):
        idx = self.q_listbox.curselection()
        if not idx: return
        i = idx[0]
        updated = {
            "question": self.edit_q_text.get(),
            "options": {k: self.edit_options[k].get() for k in self.edit_options},
            "answer": self.edit_correct.get().upper()
        }
        self.q_data[i] = updated
        self.save_question_changes()
        self.edit_msg.config(text="Question updated", fg="green")

    def delete_question(self):
        idx = self.q_listbox.curselection()
        if not idx: return
        self.q_data.pop(idx[0])
        self.save_question_changes()
        self.load_questions_list()
        self.edit_msg.config(text="Question deleted", fg="green")

    def save_question_changes(self):
        level = self.edit_level_var.get()
        file = os.path.join(DATA_DIR, f"level{level}_questions.json")
        with open(file, "w") as f:
            json.dump(self.q_data, f, indent=2)

    def render_clear_qtab(self):
        for w in self.qtab.winfo_children(): w.destroy()


if __name__ == "__main__":
    AdminConsole()
