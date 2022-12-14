import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from controlDB import C_Salas, C_Reservas, C_Funciones
import utils.generic as utl
from datetime import datetime, timedelta


class Hacer_Reserva(tk.Toplevel):
    def __init__(self,idsala,id_cliente):
        super().__init__()
        self.id_cliente=id_cliente
        self.idsala=idsala
        self.title(f'CLIENTE Id: {self.id_cliente}')
        self.grab_set()
        utl.centrar_ventana(self,1150,850)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=3)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(0,weight=1)
        mainframe.rowconfigure(1,weight=30)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        # Faja superior
        faja = tk.Frame(mainframe,bg=DARKCOLOR)
        faja.grid(row=0,column=0, columnspan=2, sticky ="nsew")
        faja.rowconfigure(0,weight=1)
        faja.rowconfigure(1,weight=8)
        tk.Label(faja, text=' CINEMARK', font = MAINBAR, bg=DARKCOLOR, fg='white' ).grid(row=1,column=1)

        # Recupero todos los datos de la funciones disponibles para la sala desde funciones y armo listas con dias, nombre de dias y horarios
        fun=C_Funciones()
        datos=fun.dia_y_hora(self.idsala)
        self.lista_dias_str=[x[0] for x in datos[0]]
        horarios=[x[0] for x in datos[1]]
        nombre_dias=[utl.nombre_dias(x) for x in self.lista_dias_str]
        
        # Recupero todos los datos sobre la sala de la pelicula elegida
        sal_DB=C_Salas()
        sala=list(sal_DB.datos_completos(self.idsala)[0])
 
        self.sala=sala  # Guardo toda la informacion sobre la sala (pelicula sinpsis etc por si queremos agragae mas info en esta interfaz)
 
        # Marco de widgets reservas
        resframe=tk.Frame(mainframe,bg=BACKGROUND)  # Guardo una referencia al marco 
        self.resframe=resframe
        
        for i in range(7) : resframe.columnconfigure(i,weight=1) #creo 5 columnas iguales
        resframe.grid(row=1,column=0,sticky ="nsew",padx=50,pady=(40,15))
        
        nombre_pelicula=ttk.Label(resframe, text=f' {sala[1]}',font = MAINBAR).grid(row=1,column=0,pady=20,columnspan=4, sticky='w')
        ttk.Label(resframe, text=f' DIAS:',font = TITLE).grid(row=2,column=0,pady=15,padx=20,columnspan=4,sticky='w')

        #Armo los Radio butyons
        self.dia_reserva=tk.StringVar()
      
        for  ind,dia in enumerate(nombre_dias):
            r = ttk.Radiobutton(resframe, text=dia.capitalize(), value=self.lista_dias_str[ind], variable=self.dia_reserva)
            r.grid(row=3,column=ind,pady=5)
        self.dia_reserva.set(self.lista_dias_str[0])  # Inicializa la varible del dia al dia [0]

        ttk.Label(resframe, text=f' HORARIOS:',font = TITLE).grid(row=4,column=0,pady=(40,15),padx=20,columnspan=4,sticky='w')

        self.hora_reserva=tk.StringVar()

        for  ind,hora in enumerate(horarios):
            r = ttk.Radiobutton(resframe, text=hora, value=hora, variable=self.hora_reserva)
            r.grid(row=5,column=ind,pady=5)  
        self.hora_reserva.set(horarios[0])  # Inicializa la varible hora [0]

        btn_reservar=ttk.Button(resframe, text="  RESERVAR  " , command=self.comprar , style='flat.TButton',padding=35 )
        btn_reservar.grid(row=12,column=0,columnspan=2, rowspan=3,padx=20,pady=20,sticky='w')
        btn_cancelar=ttk.Button(resframe, text="  CANCELAR  " , command=self.salir , style='cancel.TButton',padding=32 )
        btn_cancelar.grid(row=12,column=2,columnspan=2, rowspan=3,padx=20,pady=20,sticky='w')

        # Spinbox para elegir butacas
        ttk.Label(resframe, text=f' CANTIDAD DE ASIENTOS:',font = TITLE).grid(row=6,column=0,pady=(40,15),padx=20,columnspan=4,sticky='w')

        self.cant_butacas=tk.StringVar()
        butacas = ttk.Spinbox(resframe, from_=1, to=10, textvariable=self.cant_butacas, font=TITLE ,width=5  ,wrap=True)
        butacas.grid(row=7,column=0,pady=15,padx=40,sticky='w')
        self.cant_butacas.set(1)



    def comprar(self):
        hora=self.hora_reserva.get()
        #print(horario)
        dia_fun = self.dia_reserva.get()
        #print(dia_fun,horario)
        butacas=int(self.cant_butacas.get())
        fun=C_Funciones()
        funcion=fun.encontrar_id(self.sala[0],dia_fun, hora)
        print(fun.butacas_libres(funcion))
        if fun.butacas_libres(funcion)>=butacas:
            fun.reservar_asiento(funcion,butacas) # Disminuyo el numero de butacas disponibles en funcion de las compradas
            #print(self.id_cliente,funcion,butacas,'activa')
            res=C_Reservas()
            res.insertar(self.id_cliente,funcion,butacas,'activa' )
            self.destroy()
        else:
            messagebox.showwarning(message="NO HAY SUFICIENTES ASIENTOS DISPONIBLES", title="Lo Lamentamos")
    
    def salir(self):
        self.destroy()