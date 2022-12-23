import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from controlDB import *
from hacer_reserva import Hacer_Reserva
from gestion_reservas import Gestion_Reservas
import utils.generic as utl


class Cliente(tk.Tk):
    def __init__(self,id):
        super().__init__()
        self.id=id
        con=C_Usuarios()
        self.nombre=con.nombre(self.id)
        utl.centrar_ventana(self,1200,945)
        self.title(f'CLIENTE Id: {self.id}')
        self.iconbitmap(image_path+"\\favicon.ico")
        
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=2)
        mainframe.rowconfigure(1,weight=20)
        mainframe.rowconfigure(2,weight=1)
        mainframe.rowconfigure(3,weight=40)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        #Estilo 
        s = ttk.Style(mainframe)
        s.theme_use('clam')
        s.configure('TButton', relief='flat' ,font = TITLE, foreground="white", background=BUTTONCOL )
        s.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', BUTTONPRESS ),('disabled','grey' ), ('active', BUTTONHOV)])
        s.configure('TLabel', relief='flat' , background=BACKGROUND,foreground=DARKCOLOR )
        s.configure('grey.TButton', relief='flat' ,font = TITLE, foreground=BACKGROUND, background=BUTTONCLEAR )
        s.configure('cancel.TButton', relief='flat' ,font = TITLE, foreground="white", background=REDBUTTON )
        s.configure('grey.TLabel', background=BACKGROUND, foreground=BUTTONPRESS)
        s.configure('TRadiobutton', font = STDFONT,  background=BACKGROUND )
        s.configure('TSpinbox', font = TITLE,  arrowsize=12 )

        # Faja superior
        topframe = tk.Frame(mainframe, bg=DARKCOLOR, width=1200, height=80)
        topframe.grid(row=0, sticky="ew")
        topframe.grid_columnconfigure(0, weight=1)
        topframe.grid_rowconfigure(0, weight=1)
        topframe.grid_propagate(False)
        encabezado_izq = tk.Label(topframe, text="CINEMARK", background=DARKCOLOR, fg="white", font=MAINBAR)
        encabezado_izq.grid(row=0,padx=20, sticky=tk.W)

        # Cartelera con peliculas clikeables 
        cartframe=tk.Frame(mainframe,bg=BACKGROUND)
        cartframe.grid(row=1,column=0,sticky ="nsew")
        #cartframe.configure(borderwidth=5,relief='groove')
        for i in range(5) : cartframe.columnconfigure(i,weight=1) #creo 5 columnas iguales
        
        ttk.Label(cartframe, text=' COMPRA TU ENTRADA',font = TITLEBOLD).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=(30,10),padx=10)

        salas=C_Salas() # Leo las peliculas en cartelera
        peliculas=salas.datos_cartelera()
        # Inicializo el espacio para las salas y objetos PhotoImage
        self.sala = {}
        self.img = {}

        HEIGTH=342 # setea la altura del label (deberia ser igual a la altura de la imagen de la pelicula )
        for ind,peli in enumerate(peliculas):

            self.img[ind] = tk.PhotoImage(file= image_path +'\\' + peli[2], height=HEIGTH)
            
            self.sala[ind] = Label_con_retorno(cartframe, self.img[ind], peli[0],self.id,self)
            self.sala[ind].grid(row=2,column=ind,padx=10)
            self.sala[ind].bind('<Button-1>',self.sala[ind].reservar_funcion)
            
            ttk.Label(cartframe, text=f'{peli[1]}',font = TITLE).grid(row=1,column=ind,pady=5)    
            ttk.Label(cartframe, text=f'SALA {peli[0]}',font = TITLEBOLD).grid(row=3,column=ind,pady=5)

       
        #separador central / inferior
        sep_inf=ttk.Separator(mainframe, orient='horizontal')
        sep_inf.grid(row=2,column=0,columnspan=2, sticky='WE',pady=(50,5), padx=20)
       
        # Marco de gestionar reservas
        frame_inf = tk.Frame(mainframe, background=BACKGROUND , width=900, height=350)
        frame_inf.grid(row=3, sticky=tk.W)
        frame_inf.grid_propagate(False)

        frame_inf.grid_columnconfigure(0,weight=5)
        frame_inf.grid_columnconfigure(1,weight=2)
        frame_inf.grid_columnconfigure(2,weight=3)
        frame_inf.grid_columnconfigure(3,weight=3)

        #Entrada de datos para ver y borrar reservas
        label_entry_titulo = ttk.Label(frame_inf, text=f"Tus Reservas {self.nombre}", font=TITLEBOLD)
        label_entry_titulo.grid(row=0,column=0, padx=20, sticky="w", pady=(30,20), columnspan=3)

        con_res= C_Reservas()
        self.reservas=con_res.reservas_activas_por_cliente(self.id)  # Leo todas las reservas del cliente
        
        # Obtengo los datos de las funciones y salas correspondientes a cada reserva
        self.lista_funciones=[]
        if len(self.reservas)>0:
            con_func=C_Funciones()
            for reserva in self.reservas :
                id_funcion=reserva[1]
                fun=con_func.datos_funcion(id_funcion)

                conex_salas= C_Salas()
                lista_sala=conex_salas.datos_completos(fun[0])
                self.lista_funciones.append(f'  - Sala{fun[0]} | {fun[1]} Hs: {fun[2]} | {lista_sala[1]}')   

        
        list_reservas = tk.Variable(value=self.lista_funciones)
        self.lb_res = tk.Listbox(frame_inf, listvariable = list_reservas,height=10, bd=0,font=STDFONT,)
        self.lb_res.grid(row=1,column=0,padx=20, sticky="WE", columnspan=3)


        
        # ** Agregar las funciones para ir a modificar y para eliminar las peliculas
        btn_mPelicula=ttk.Button(frame_inf, text="Eliminar " ,command=self.eliminar_reserva,  style='cancel.TButton',padding=10).grid(row=1,column=3,padx=5,sticky='NW')

        self.mainloop()
    
    def eliminar_reserva(self):
        index = self.lb_res.curselection()
        if (len(index)==0):
            return
        indice = index[0]
        self.actualizar_reservas()
        id = self.reservas[indice][0]
        
        conex_res=C_Reservas()
        conex_res.eliminar_reserva(id)   #elimina la reserva elegida de la Base de datos
        butacas = self.reservas[indice][2] # butacas comprometidas en la reserva, hay que liberarls, incrementando butacalibres en tabla funciones
        id_funcion=self.reservas[indice][1]
        con_fun=C_Funciones()
        con_fun.liberar_asiento(id_funcion, butacas)
        self.lb_res.delete(indice) # Esto elimina la reserva de la ventana listbox, no de la base de datos

    
    def actualizar_reservas(self):
            con_res= C_Reservas()
            self.reservas=con_res.reservas_activas_por_cliente(self.id)  # Leo todas las reservas del cliente
            self.lista_funciones=[]
            if len(self.reservas)>0:
                con_func=C_Funciones()
                for reserva in self.reservas :
                    id_funcion=reserva[1]
                    fun=con_func.datos_funcion(id_funcion)

                    conex_salas= C_Salas()
                    lista_sala=conex_salas.datos_completos(fun[0])
                    self.lista_funciones.append(f'  - Sala{fun[0]} | {fun[1]} Hs: {fun[2]} | {lista_sala[1]}')
             
            list_reservas = tk.Variable(value=self.lista_funciones)
            self.lb_res.config(listvariable = list_reservas)  


    
# Boton que guarda la info de a que Id de sala corresponde cuando lo crean   
class Label_con_retorno(tk.Label): 
    def __init__(self,parent,img,idsala,id_cliente,root): #Recibe el parent para el boton, el objeto PhotoImage y el id de la sala a la que corresponden
        super().__init__(parent, image=img)
        self.root=root
        self.idsala=idsala 
        self.id_cliente=id_cliente

    def reservar_funcion(self,event):
        res = Hacer_Reserva(self.idsala,self.id_cliente)  # Abre el popup para hacer la reserva
        self.root.wait_window(res)
        self.root.actualizar_reservas()
    
       
 


Cliente(12)




