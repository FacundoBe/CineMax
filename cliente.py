import tkinter as tk
from tkinter import ttk
from settings import *
from controlDB import C_Usuarios, C_Salas
from hacer_reserva import Hacer_Reserva
from gestion_reservas import Gestion_Reservas
import utils.generic as utl

class Cliente(tk.Tk):
    def __init__(self,id):
        super().__init__()
        self.id=id
        con=C_Usuarios()
        self.nombre=con.nombre(self.id)
        utl.centrar_ventana(self,1200,900)
        self.title(f'CLIENTE Id: {self.id}')
        self.iconbitmap(image_path+"\\favicon.ico")
        
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=2)
        mainframe.rowconfigure(1,weight=20)
        mainframe.rowconfigure(2,weight=60)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        #Estilo 
        s = ttk.Style(mainframe)
        s.theme_use('clam')
        s.configure('TButton', relief='flat' ,font = TITLE, foreground="white", background=BUTTONCOL )
        s.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', BUTTONPRESS ),('disabled','grey' ), ('active', BUTTONHOV)])
        s.configure('TLabel', relief='flat' , background=BACKGROUND )
        s.configure('grey.TButton', relief='flat' ,font = TITLE, foreground=BACKGROUND, background=BUTTONCLEAR )
        s.configure('cancel.TButton', relief='flat' ,font = TITLE, foreground="white", background=REDBUTTON )
        s.configure('grey.TLabel', background=BACKGROUND, foreground=BUTTONPRESS)
        s.configure('TRadiobutton', font = TITLE,  background=BACKGROUND )
        s.configure('TSpinbox', font = TITLE,  arrowsize=14 )

        # Faja superior
        faja = tk.Frame(mainframe,bg=DARKCOLOR)
        faja.grid(row=0,column=0, columnspan=2, sticky ="nsew")
        faja.rowconfigure(0,weight=1)
        faja.rowconfigure(1,weight=8)
        tk.Label(faja, text=' CINEMARK', font = MAINBAR, bg=DARKCOLOR, fg='white' ).grid(row=1,column=1)

        # Cartelera
        cartframe=tk.Frame(mainframe,bg=BACKGROUND)
        cartframe.grid(row=1,column=0,sticky ="nsew")
        #cartframe.configure(borderwidth=5,relief='groove')
        for i in range(5) : cartframe.columnconfigure(i,weight=1) #creo 5 columnas iguales
        
        ttk.Label(cartframe, text=' COMPRA TU ENTRADA',font = TITLEBOLD).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=(40,20),padx=10)

        salas=C_Salas() # Leo las peliculas en cartelera
        peliculas=salas.datos_cartelera()
        # Inicializo el espacio para las salas y objetos PhotoImage
        self.sala = {}
        self.img = {}

        HEIGTH=342 # setea la altura del label (deberia ser igual a la altura de la imagen de la pelicula )
        for ind,peli in enumerate(peliculas):

            self.img[ind] = tk.PhotoImage(file= image_path +'\\' + peli[2], height=HEIGTH)
            
            self.sala[ind] = Label_con_retorno(cartframe, self.img[ind], peli[0],self.id)
            self.sala[ind].grid(row=2,column=ind,padx=10)
            self.sala[ind].bind('<Button-1>',self.sala[ind].reservar_funcion)
            
            ttk.Label(cartframe, text=f'{peli[1]}',font = TITLE).grid(row=1,column=ind,pady=5)    
            ttk.Label(cartframe, text=f'SALA {peli[0]}',font = TITLEBOLD).grid(row=3,column=ind,pady=5)

        # Marco de gestionar reservas
        resframe=tk.Frame(mainframe,bg=BACKGROUND)
        resframe.grid(row=2,column=0,sticky ="nsew")
        #resframe.configure(borderwidth=5,relief='groove')
        
        ttk.Label(resframe, text=' GESTIONA TUS RESERVAS',font = TITLEBOLD).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=20,padx=10)
        ttk.Button(resframe, text="  VER RESERVAS  " , command=self.llama_gestion_reservas , style='flat.TButton',padding=35 ).grid(row=2,column=0)



        self.mainloop()
    
    def llama_gestion_reservas(self):
        Gestion_Reservas(self.id)

   
# Boton que guarda la info de a que Id de sala corresponde cuando lo crean   
class Label_con_retorno(tk.Label): 
    def __init__(self,parent,img,idsala,id_cliente): #Recibe el parent para el boton, el objeto PhotoImage y el id de la sala a la que corresponden
        super().__init__(parent, image=img)
        self.idsala=idsala 
        self.id_cliente=id_cliente

    def reservar_funcion(self,event):
        Hacer_Reserva(self.idsala,self.id_cliente)  # Abre el popup para hacer la reserva

Cliente(4)


