import tkinter as tk
from tkinter import ttk
from settings import *
import utils.generic as utl

class Gestion_Reservas(tk.Toplevel):
    def __init__(self,id_cliente):
        super().__init__()
        self.id_cliente=id_cliente
        self.title(f'CLIENTE Id: {self.id_cliente}')
        self.grab_set()
        utl.centrar_ventana(self,1150,850)
        ttk.Label(self, text=f' AQUI HAY QUE MOSTRAR LAS RESERVAS DEL CLIENTE \n Y PERMITIRLE BORRAR O MODIFICAR',font = MAINBAR).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=40,padx=10)