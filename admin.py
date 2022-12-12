import tkinter as tk
from tkinter import ttk
from settings import *

class Admin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x900')
        self.title('ADMINISTRADOR')
        self.iconbitmap("img\\favicon.ico")
        
        
        self.mainloop()