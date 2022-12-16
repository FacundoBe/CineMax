import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from controlDB import *
import utils.generic as utl
from datetime import datetime, timedelta


class Hacer_Reserva(tk.Toplevel):
    def __init__(self,idsala,id_cliente):
        super().__init__(background=BACKGROUND)
        self.attributes('-alpha',0.99)                 # Le da transparencia al fondo de la ventana (casi nada)
        self.id_cliente=id_cliente
        self.idsala=idsala
        self.title(f'CLIENTE Id: {self.id_cliente}')
        self.grab_set()
        utl.centrar_ventana(self,1200,900)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=3)
        mainframe.rowconfigure(0,weight=1)
        mainframe.rowconfigure(1,weight=30)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH, padx=190)  

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
        print(horarios)
        # Recupero todos los datos sobre la sala de la pelicula elegida
        sal_DB=C_Salas()
        sala=list(sal_DB.datos_completos(self.idsala)[0])
        self.sala=sala  # Guardo toda la informacion sobre la sala (pelicula sinpsis etc por si queremos agragae mas info en esta interfaz)
 
        
        # Pelicula Lateral 
        cartframe=tk.Frame(mainframe,bg=BACKGROUND)
        cartframe.grid(row=1,column=0,sticky ="nsew")
        HEIGTH=342 # setea la altura del label (deberia ser igual a la altura de la imagen de la pelicula )
        self.img = tk.PhotoImage(file= image_path +'\\' + sala[3], height=HEIGTH)
        imagen_pelicula = tk.Label(cartframe,image=self.img).grid(row=0,column=0,padx=(40,0),pady=(70,15))            
        ttk.Label(cartframe, text=f'SALA {sala[0]}',font = TITLEBOLD).grid(row=3,column=0,pady=5)    
        

        # Marco de widgets reservas
        resframe=tk.Frame(mainframe,bg=BACKGROUND)  # Guardo una referencia al marco 
        self.resframe=resframe
        
        for i in range(7) : resframe.columnconfigure(i,weight=1) #creo 5 columnas iguales
        resframe.grid(row=1,column=1,sticky ="nsew",pady=(40,15))
        
        nombre_pelicula=ttk.Label(resframe, text=f' {sala[1]}',font = MAINBAR).grid(row=1,column=0,pady=(20,0),columnspan=4, sticky='w')
        ttk.Label(resframe, text=f' Dias:',font = TITLE).grid(row=2,column=0,pady=(20,5),padx=20,columnspan=4,sticky='w')

        #Armo los Radio buttons
        self.dia_reserva=tk.StringVar()
      
        for  ind,dia in enumerate(nombre_dias):
            r = ttk.Radiobutton(resframe, text=dia.capitalize(), value=self.lista_dias_str[ind], variable=self.dia_reserva)
            rw=3
            if ind>3:       #para distribuirlo en en filas de 4 y de ahi baja a la siguiente fila
                ind = ind -4
                rw=4
            r.grid(row=rw,column=ind,pady=5)
        self.dia_reserva.set(self.lista_dias_str[0])  # Inicializa la varible del dia al dia [0]

        ttk.Label(resframe, text=f' Horarios:',font = TITLE).grid(row=5,column=0,pady=(20,5),padx=20,columnspan=6,sticky='w')

        self.hora_reserva=tk.StringVar()

        for  ind,hora in enumerate(horarios):
            r = ttk.Radiobutton(resframe, text=hora, value=hora, variable=self.hora_reserva)
            r.grid(row=6,column=ind,pady=5)  
        self.hora_reserva.set(horarios[0])  # Inicializa la varible hora [0]

        btn_reservar=ttk.Button(resframe, text=" RESERVAR " , command=self.comprar , style='flat.TButton',padding=20 )
        btn_reservar.grid(row=12,column=0,columnspan=2, rowspan=3,padx=20,pady=20,sticky='w')
        btn_cancelar=ttk.Button(resframe, text=" CANCELAR " , command=self.salir , style='cancel.TButton',padding=17 )
        btn_cancelar.grid(row=12,column=2,columnspan=2, rowspan=3,padx=20,pady=20,sticky='w')

        # Spinbox para elegir butacas
        ttk.Label(resframe, text=f' Cantidad de Asientos:',font = TITLE).grid(row=7,column=0,pady=(20,0),padx=20,columnspan=4,sticky='w')

        self.cant_butacas=tk.StringVar()
        butacas = ttk.Spinbox(resframe, from_=1, to=10, textvariable=self.cant_butacas, font=STDFONT ,width=5  ,wrap=True)
        butacas.grid(row=8,column=0,pady=15,padx=40,sticky='w')
        self.cant_butacas.set(1)

        self.confirmada=0  # Aqui se guarda un flag de confirmacion o no de la reserva al apretar el boton reservar



    def comprar(self):
        hora=self.hora_reserva.get()
        dia_fun = self.dia_reserva.get()
        desc_con=C_Descuentos()
        descuento=desc_con.descuento(utl.nombre_dias(dia_fun))  # lee de la base de datos el descuento que toca al dia de la reserva
        butacas=int(self.cant_butacas.get())
        fun=C_Funciones()
        funcion=fun.encontrar_id(self.sala[0],dia_fun, hora)
        Vent_confirma(self,descuento,butacas)  # llamo a la ventana de conformacion de reservas donde muestro precio y descuentos
        if self.confirmada==1: # Esto se ejecuta si el se presiona el botn confirmar que cambia self.confirmada a 1
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
    

class Vent_confirma(tk.Toplevel):
    def __init__(self,parent,descuento,cant_butacas):
        super().__init__(parent)
        self.parent=parent # La guardo como attributo asi el metodo que genera el boton la puede usar directamente
        self.title('Confirmar Reserva')
        utl.centrar_ventana(self,500,290)
        frame=tk.Frame(self, background=BACKGROUND)         
        frame.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        frame.columnconfigure(0,weight=1) 
        frame.columnconfigure(1,weight=1)
        usr=C_Usuarios()
        nombre=usr.nombre(parent.id_cliente)
        ttk.Label(frame, text=f'  SU RESERVA: {nombre}',font = TITLEBOLD).grid(row=0,column=0,columnspan=2,pady=20,sticky='w')
        ttk.Label(frame, text=f' TOTAL: {PRECIO*cant_butacas}',font = TITLE).grid(row=1,column=0,columnspan=2,padx=(10,0))
        ttk.Label(frame, text=f'CON DESCUENTO: {PRECIO*cant_butacas*(1-descuento/100)} ',font = TITLE).grid(row=2,column=0,columnspan=2,padx=(10,0),pady=(15,30))   
        btn_confirma=ttk.Button(frame, text="CONFIRMAR" , command=self.confirma , style='flat.TButton',padding=5 )
        btn_confirma.grid(row=3,column=0, rowspan=3,padx=40,pady=20,sticky='w')
        btn_cancela=ttk.Button(frame, text="CANCELAR" , command=self.destroy , style='cancel.TButton',padding=4 )
        btn_cancela.grid(row=3,column=1,columnspan=2, rowspan=3,padx=20,pady=20,sticky='w')
        self.wait_window(self)  # Se pausa todo hasta que esta ventana se cierre
        
    def confirma(self): #Cambia el valor de del atributo confirmada de hacer reserva a 1 lo que permite que se escriba la reserva a BD 
        self.parent.confirmada=1
        self.destroy()