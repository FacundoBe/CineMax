import tkinter as tk
from tkinter import ttk

class Cliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x900')
        self.title('CLIENTE')
        self.mainloop()