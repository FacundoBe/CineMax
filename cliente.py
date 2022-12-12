import tkinter as tk
from tkinter import ttk
from settings import *
from controlDB import C_Usuarios
import utils.generic as utl

class Cliente(tk.Tk):
    def __init__(self,id):
        super().__init__()
        self.id=id
        con=C_Usuarios()
        self.nombre=con.nombre(self.id)
        self.geometry('1200x900')
        utl.centrar_ventana(self,1200,900)
        self.title(f'CLIENTE Id: {self.id}')
        self.iconbitmap("img\\favicon.ico")
        ttk.Label(self, text=f'Bienvenido {self.nombre}', font=MAINBAR).grid(sticky='w')
        
        
        self.mainloop()

