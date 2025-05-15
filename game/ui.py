import tkinter as tk
from game.levels import GameLevels

def launch_game():
    root = tk.Tk()
    game = GameLevels(root)
    root.mainloop()