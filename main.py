from tkinter import Tk
from game.login import login_screen

if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)
    login_screen(root)
    root.mainloop()
