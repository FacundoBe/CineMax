import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from cliente import Cliente
from controlDB import C_Usuarios
import utils.generic as utl
import re


class Registro(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('CREAR NUEVA CUENTA')
        self.iconbitmap(image_path+'/favicon.ico')
        utl.centrar_ventana(self,1200,900)
        self.resizable(False, False)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=1)
        mainframe.rowconfigure(1,weight=15)
        mainframe.rowconfigure(2,weight=15)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        # Faja superior
        faja = tk.Frame(mainframe,bg=DARKCOLOR)
        faja.grid(row=0,column=0, columnspan=2, sticky ="nsew")
        faja.rowconfigure(0,weight=1)
        faja.rowconfigure(1,weight=8)
        tk.Label(faja, text=' CINEMARK', font = MAINBAR, bg=DARKCOLOR, fg='white' ).grid(row=1,column=1)

        # Marco del Registro
        logframe=tk.Frame(mainframe,bg=BACKGROUND, width=200)
        self.logframe=logframe                      #Guardo una referencia al marco de login/registro
        logframe.columnconfigure(0,weight=2)
        logframe.columnconfigure(1,weight=2)
        logframe.grid(row=1,column=0,sticky ="nsew",padx=300,pady=25)
        
        # Aplico Estilo general a botones y eiquetas (TButton y TLabel )
        s = ttk.Style(logframe)
        s.theme_use('clam')
        s.configure('TButton', relief='flat' ,font = TITLE, foreground="white", background=BUTTONCOL )
        s.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '!disabled',BUTTONPRESS ), ('active', BUTTONHOV)])
        s.configure('TLabel', relief='flat' , background=BACKGROUND )

        # Widgets del login
        ttk.Label(logframe, text='CREAR NUEVA CUENTA',font = TITLE).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=(20,35))
        ttk.Label(logframe, text='* Nombre:',font = STDFONT).grid(row=1,column=0,sticky='w',pady=7)
        ttk.Label(logframe, text='* Apellido:',font = STDFONT).grid(row=1,column=1,sticky='w',pady=7)
        ttk.Label(logframe, text='* Email:',font = STDFONT).grid(row=3,column=0,sticky='w',pady=(40,7))
        ttk.Label(logframe, text='* Contraseña:',font = STDFONT).grid(row=5,column=0,sticky='w',pady=(40,7))
        ttk.Label(logframe, text='* Confirmar Contraseña:',font = STDFONT).grid(row=5,column=1,sticky='w',pady=(40,7))
        ttk.Label(logframe, text='Numero de telefono',font = STDFONT).grid(row=7,column=0,sticky='w',pady=(40,7))
        
        # variable de los entry del tkinter para recuperar las entradas 
        self.nombre = tk.StringVar()
        self.apellido = tk.StringVar()
        self.email = tk.StringVar()
        self.passw1 = tk.StringVar()
        self.passw2 = tk.StringVar()
        self.tel = tk.StringVar()
        
        # Widgets Entry
        tk.Entry(logframe, textvariable = self.nombre, font=STDFONT,bd=0,width=23).grid(row=2,column=0,sticky='w',ipady=4)
        tk.Entry(logframe, textvariable = self.apellido, font=STDFONT,bd=0,width=23).grid(row=2,column=1,sticky='w',ipady=4)
        tk.Entry(logframe, textvariable = self.email, font=STDFONT,bd=0, width=52).grid(row=4,column=0,columnspan=2,sticky='w',ipady=4)
        tk.Entry(logframe, textvariable = self.passw1, show='*', font=STDFONT,bd=0,width=23).grid(row=6,column=0,sticky='w',ipady=4)
        tk.Entry(logframe, textvariable = self.passw2, show='*', font=STDFONT,bd=0,width=23).grid(row=6,column=1,sticky='w',ipady=4)
        tk.Entry(logframe, textvariable = self.tel,  font=STDFONT,bd=0,width=52).grid(row=8,column=0,columnspan=2,sticky='w',ipady=4)
        
        ttk.Label(logframe, text='* Campos obligatorios',font = SMALLFONT).grid(row=9,column=0,sticky='nw',pady=10)
        btn_reg=ttk.Button(logframe, text=" REGISTRARSE " , command=self.guardar, style='flat.TButton',padding=20).grid(row=9,column=1, pady=(40,7),padx=10,sticky='w')

        self.mainloop() #ejecuto el mainloop de registro

    def validar_mail(self,email):
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat,email):
            return True
        return False

    def guardar(self):
        nombre=self.nombre.get()
        apellido=self.apellido.get()
        email=self.email.get()
        passw1=self.passw1.get()
        passw2=self.passw2.get()
        tel=self.tel.get()
        if nombre!="" and apellido != "" and email != "" and passw1!="" and passw2!="": # verifica que los campos obligatorion no esten vacios
            if self.validar_mail(email): # verifica que el emil tenga el formato correcto
                con=C_Usuarios()
                if not con.esusuario(email):  # Si el usuario no esta registrado sigue las comprobaciones
                    if passw2==passw1:# La contraseña y verificacion coinciden
                        if len(passw2)>=6:
                            con.insertar(nombre,apellido, email,passw1,0,tel) # Guarda los valores introducidos en la tabla 
                            val=con.validar(email,passw1)
                            self.destroy()                                    # usuarios con permisos de cliente (permisos=0)
                            Cliente(val[0])
                        else: # Longitud de contraseña menos a 6 digitos
                            messagebox.showwarning(message=f"La contraseña debe tener al menos 6 caracteres {email} *", title="Error")
                    else: #Contraseña y confirmacion no coincide
                        messagebox.showwarning(message=f"Las contraseñas ingresadas no coinciden ", title="Error")
                else:                                                                 
                    messagebox.showwarning(message=f"Ya existe un usuario registrado con el email: {email} ", title="Error")
            else:
                messagebox.showwarning(message=f" {email} no es un Email valido: ", title="Error")
        else:
            messagebox.showwarning(message="Debe completar todos los campos con *", title="Error")

        
 


