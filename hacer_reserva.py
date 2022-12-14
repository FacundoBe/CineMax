import tkinter as tk
from tkinter import ttk
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
        
        # Recupero todos los datos de la funciones disponibles para la pelicula elegida
        sal_DB=C_Salas()
        sala=list(sal_DB.datos_completos(self.idsala)[0])
        sala[5]=sala[5].replace(" ", "") #le saco el espacio
        sala[5]=sala[5].split(',')              # Convierto los horarios en una lista de listas con formato [[HH:MM], [HH:MM], etc.  ]
        print(sala[5])
        self.sala=sala
        ahora= datetime.now()
        self.lista_dias=[]
        nombre_dias=[]
        for pos in range(0,7):
                dia_fun = ahora + timedelta(days=pos) #Voy sumandole un dia mas a la fecha por ciclo
                self.lista_dias.append(dia_fun)  # lista de fechas de los proximos 7 dias en formato datetime
                nombre_dias.append(dia_fun.strftime('%A')) #nombre de los proximos 7 dias en string 
                
   
        # Marco de widgets reservas
        resframe=tk.Frame(mainframe,bg=BACKGROUND)  # Guardo una referencia al marco 
        self.resframe=resframe
        resframe.columnconfigure(0,weight=2)        
        resframe.columnconfigure(1,weight=2)
        resframe.columnconfigure(3,weight=2)
        resframe.columnconfigure(4,weight=2)
        resframe.columnconfigure(5,weight=2)
        resframe.grid(row=1,column=0,sticky ="nsew",padx=50,pady=(40,15))
        
        nombre_pelicula=ttk.Label(resframe, text=f' {sala[1]}',font = MAINBAR).grid(row=1,column=0,pady=20,columnspan=4, sticky='w')
        ttk.Label(resframe, text=f' DIAS:',font = TITLE).grid(row=2,column=0,pady=5,padx=20,columnspan=4,sticky='w')

        self.dia_reserva=0
        self.hora_reserva=0
        self.dia=[0,0,0,0,0,0,0]
        self.horario_bt=[0,0,0,0]

        self.dia[0]= ttk.Button(resframe, text=f"  Hoy " , command=self.dia1 , style='flat.TButton' ,padding=5 )
        self.dia[0].grid(row=3,column=0)
        self.dia[1]= ttk.Button(resframe, text=f"Mañana" , command=self.dia2 , style='flat.TButton',padding=5 )
        self.dia[1].grid(row=3,column=1,pady=5)
        self.dia[2]= ttk.Button(resframe, text=f"{nombre_dias[2].capitalize()}" , command=self.dia3 , style='flat.TButton',padding=5 )
        self.dia[2].grid(row=3,column=2,pady=5)
        self.dia[3]= ttk.Button(resframe, text=f"{nombre_dias[3].capitalize()}" , command=self.dia4 , style='flat.TButton',padding=5 )
        self.dia[3].grid(row=3,column=3,pady=5)
        self.dia[4]= ttk.Button(resframe, text=f"{nombre_dias[4].capitalize()}" , command=self.dia5 , style='flat.TButton',padding=5 )
        self.dia[4].grid(row=4,column=0,pady=5)
        self.dia[5]= ttk.Button(resframe, text=f"{nombre_dias[5].capitalize()}" , command=self.dia6 , style='flat.TButton',padding=5 )
        self.dia[5].grid(row=4,column=1,pady=5)
        self.dia[6]= ttk.Button(resframe, text=f"{nombre_dias[6].capitalize()}" , command=self.dia7 , style='flat.TButton',padding=5 )
        self.dia[6].grid(row=4,column=2,pady=5)
    
        self.butacas = tk.StringVar()
        self.butacas_entry= tk.Entry(self.resframe, textvariable = self.butacas, width=15 , font=STDFONT,bd=0)

    def dia1(self):
        for i in range(1,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[0].configure(style='flat.TButton')
        self.dia_reserva=0
        self.horario()

    def dia2(self):
        for i in range(0,1) : self.dia[i].configure(style='grey.TButton')
        for i in range(2,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[1].configure(style='flat.TButton')
        self.dia_reserva=1
        self.horario()

    def dia3(self):
        for i in range(0,2) : self.dia[i].configure(style='grey.TButton')
        for i in range(3,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[2].configure(style='flat.TButton')
        self.dia_reserva=2
        self.horario()

    def dia4(self):
        for i in range(0,3) : self.dia[i].configure(style='grey.TButton')
        for i in range(4,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[3].configure(style='flat.TButton')
        self.dia_reserva=3
        self.horario()
    
    def dia5(self):
        for i in range(0,4) : self.dia[i].configure(style='grey.TButton')
        for i in range(5,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[4].configure(style='flat.TButton')
        self.dia_reserva=4
        self.horario()

    def dia6(self):
        for i in range(0,5) : self.dia[i].configure(style='grey.TButton')
        for i in range(6,7) : self.dia[i].configure(style='grey.TButton')
        self.dia[5].configure(style='flat.TButton')
        self.dia_reserva=5
        self.horario()

    def dia7(self):
        for i in range(0,6) : self.dia[i].configure(style='grey.TButton')
        self.dia[6].configure(style='flat.TButton')
        self.dia_reserva=6
        self.horario()

    def horario(self):
        ttk.Label(self.resframe, text=f' HORARIO:',font = TITLE).grid(row=5,column=0,pady=(30,15),padx=20,columnspan=4,sticky='w')
        
        self.horario_bt[0]= ttk.Button(self.resframe, text=f"{self.sala[5][0]} " , command=self.bt_hora1 , style='flat.TButton' ,padding=5 )
        self.horario_bt[0].grid(row=6,column=0)
        if len(self.sala[5])>1:
            self.horario_bt[1]= ttk.Button(self.resframe, text=f"{self.sala[5][1]}" , command=self.bt_hora2 , style='flat.TButton',padding=5 )
            self.horario_bt[1].grid(row=6,column=1,pady=5)
        if len(self.sala[5])>2:
            self.horario_bt[2]= ttk.Button(self.resframe, text=f"{self.sala[5][2]}" , command=self.bt_hora3 , style='flat.TButton',padding=5 )
            self.horario_bt[2].grid(row=6,column=2,pady=5)
        if len(self.sala[5])>3:
            self.horario_bt[3]= ttk.Button(self.resframe, text=f"{self.sala[5][3]}" , command=self.bt_hora4 , style='flat.TButton',padding=5 )
            self.horario_bt[3].grid(row=6,column=3,pady=5)
    
        #SOLO FUNCIONA PARA DOS HORARIOS MEJOR RECONVERTIRLA CON UN RADIO BUTTON ***
    def bt_hora1(self):
        self.horario_bt[1].configure(style='grey.TButton')
        self.horario_bt[0].configure(style='flat.TButton')
        self.hora_reserva=self.sala[5][0]
        self.butacas_elegir()

    def bt_hora2(self):
        self.horario_bt[0].configure(style='grey.TButton')
        self.horario_bt[1].configure(style='flat.TButton')
        self.hora_reserva=self.sala[5][1]
        self.butacas_elegir()
    
        
    def butacas_elegir(self):
        ttk.Label(self.resframe, text=f'BUTACAS:',font = TITLE).grid(row=7,column=0,pady=(30,10),padx=20,columnspan=2,sticky='w')
        self.butacas_entry.grid(row=8,column=0,ipady=5,padx=25,sticky='w')
        ttk.Button(self.resframe, text="Comprar", padding=30, command=self.comprar ).grid(row=8,column=3, sticky='w' )

    def comprar(self):
        hora=self.hora_reserva.split(':')[0]
        minutos=self.hora_reserva.split(':')[1]
        #print(hora,minutos)
        dia_fun = self.lista_dias[self.dia_reserva]
        horario_funcion=datetime(dia_fun.year, dia_fun.month, dia_fun.day,int(hora),int(minutos))
        horario_str= horario_funcion.strftime('%d/%m/%Y %H:%M' )
        fun=C_Funciones()
        funcion=fun.encontrar_id(self.sala[0],horario_str)
        print(self.sala[0],horario_str)
        butacas=self.butacas.get()
        if butacas=="":
            butacas=1  #Provisorio HAy que validar bien despues ***
        print(self.id_cliente,funcion,butacas,'activa')
        res=C_Reservas()
        res.insertar(self.id_cliente,funcion,butacas,'activa' )


