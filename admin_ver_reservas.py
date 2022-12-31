import tkinter as tk
from tkinter import ttk
from settings import *
import utils.generic as utl
from tkinter import scrolledtext
from controlDB import *

class AdminVerReservas(tk.Toplevel):
    def __init__(self):
        super().__init__()
        utl.centrar_ventana(self,1200,900)
        self.iconbitmap(image_path+"\\favicon.ico")
        self.title('Ver Reservas')
        self.resizable(0,0)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=3)
        self.columnconfigure(2,weight=1)
        
        #Configuracion Grid Ventana principal
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        # Barra Superior
        topframe = tk.Frame(self, bg=DARKCOLOR, width=1000, height=80)
        topframe.grid(row=0,column=1, sticky="ew")
        topframe.grid_columnconfigure(0, weight=1)
        topframe.grid_rowconfigure(0, weight=1)
        topframe.grid_propagate(False)
        encabezado_izq = tk.Label(topframe, text="CINEMARK", background="#363636", fg="white", font=MAINBAR)
        encabezado_izq.grid(row=0,padx=20, sticky=tk.W)
        encabezado_der = tk.Label(topframe, text="CARTELERA", background="#363636", fg="white", font=("Verdana", 25))
        encabezado_der.grid(row=0, column=0, sticky=tk.E, padx=20)
        
        # Seccion de visualizacion de reservas
        frame = tk.Frame(self, width=850, height=800)
        frame.grid(row=2,column=1, sticky="N", pady=30)
        frame.grid_propagate(False)
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)
        label_titulo=tk.Label(frame, text="RESERVAS", font=TITLEBOLD).grid(row=0,column=0, padx=10, sticky="w", pady=(20,10))
        
        # Filtro
        

        label_entry_filtro = tk.Label(frame, text="Nombre", font=STDFONT)
        label_entry_filtro.grid(row=2,column=0, padx=10, sticky="w", pady=(5,10))
        self.filtro_nombre = tk.StringVar()
        entry_filtro_nombre = tk.Entry(frame, textvariable=self.filtro_nombre, font=STDFONT,width=20, bd=0)
        entry_filtro_nombre.grid(row=3, column=0, ipady=5, padx=10, sticky='w')
        
        entry_filtro_nombre.bind("<KeyRelease>",self.filtrar)


        label_entry_filtro = tk.Label(frame, text="Apellido", font=STDFONT)
        label_entry_filtro.grid(row=2,column=1, padx=10, sticky="w", pady=(5,10))
        self.filtro_apellido = tk.StringVar()
        entry_filtro_apellido = tk.Entry(frame, textvariable=self.filtro_apellido, font=STDFONT,width=20, bd=0)
        entry_filtro_apellido.grid(row=3, column=1, ipady=5, padx=10, sticky='w')
        
        entry_filtro_apellido.bind("<KeyRelease>",self.filtrar)

        label_entry_filtro = tk.Label(frame, text="Email", font=STDFONT)
        label_entry_filtro.grid(row=2,column=2, padx=10, sticky="w", pady=(5,10))
        self.filtro_email = tk.StringVar()
        entry_filtro_email = tk.Entry(frame, textvariable=self.filtro_email, font=STDFONT, width=20, bd=0)
        entry_filtro_email.grid(row=3, column=2, ipady=5, padx=(10,0), sticky='w')
        
        entry_filtro_email.bind("<KeyRelease>",self.filtrar)

        # Ventana que muestra las reservas
        self.window_reservas = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=30, font=STDFONT,bd=0)
        self.window_reservas.grid(row=4, column=0,columnspan=3, pady=20,padx=10)

        con = Consulta_Joined()
        reservas_comp_DB = con.reservas_joined() # Cargo la lista con reservas de la BD
        self.reservas_formateadas=[]                      # lo voay a pasar  de lista de tuplas a esta lista, con 4 columnas, nombre, apellido,email,reserva
        for reserva in reservas_comp_DB:
            res=f' {reserva[7]} {reserva[8]}Hs | {reserva[9]}  {reserva[5]} Butacas '
            self.reservas_formateadas.append([reserva[0], reserva[1], reserva[2], res ])

        self.llenar_ventana(self.reservas_formateadas) # inicializo con las reservas completas
        

    def llenar_ventana(self,lista):
        # Limpio la ventana que muestra las reservas
        self.window_reservas.delete("1.0",tk.END)

        for reserva in lista:
            self.window_reservas.insert(tk.END, f'{reserva[3]}  {reserva[0]} {reserva[1]} {reserva[2]}\n')
    

    def filtrar(self,e):
        nombre=self.filtro_nombre.get()
        apellido=self.filtro_apellido.get()
        email=self.filtro_email.get()
        if nombre == "" and apellido =="" and email=="":
            lista=self.reservas_formateadas
        else:
            lista=[]
            for res in self.reservas_formateadas:
                if nombre.lower() in res[0].lower() and apellido.lower() in res[1].lower() and email in res[2]: 
                    lista.append(res)
        
        self.llenar_ventana(lista)




        