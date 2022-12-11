import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from controlDB import C_Usuarios
import utils.generic as utl
from admin import Admin
from cliente import Cliente
from registro import Registro


class Login(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry('1200x900')
        self.title('LOGIN')
        self.iconbitmap("img\\favicon.ico")
        utl.centrar_ventana(self,1200,900)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=2)
        mainframe.rowconfigure(1,weight=20)
        mainframe.rowconfigure(2,weight=10)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        # Faja superior
        faja = tk.Frame(mainframe,bg=DARKCOLOR)
        faja.grid(row=0,column=0, columnspan=2, sticky ="nsew")
        faja.rowconfigure(0,weight=1)
        faja.rowconfigure(1,weight=8)
        tk.Label(faja, text=' CINEMARK', font = MAINBAR, bg=DARKCOLOR, fg='white' ).grid(row=1,column=1)

        # Marco del login
        logframe=tk.Frame(mainframe,bg=BACKGROUND)
        self.logframe=logframe                      #Guardo uan rfeecina al marco de login/registro
        logframe.columnconfigure(0,weight=2)
        logframe.columnconfigure(1,weight=2)
        logframe.columnconfigure(3,weight=1)
        logframe.columnconfigure(4,weight=2)
        logframe.columnconfigure(5,weight=2)
        logframe.grid(row=1,column=0,sticky ="nsew",padx=100,pady=(80,15))
        #logframe['borderwidth'] = 5
        #logframe['relief'] = 'groove'
        

        #Estilo 
        s = ttk.Style(logframe)
        s.theme_use('clam')
        s.configure('TButton', relief='flat' ,font = TITLE, foreground="white", background=BUTTONCOL )
        s.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', '!disabled',BUTTONPRESS ), ('active', BUTTONHOV)])
        s.configure('TLabel', relief='flat' , background=BACKGROUND )

        # Widgets del login
        ttk.Label(logframe, text='INGRESA A TU CUENTA',font = TITLE).grid(row=0,column=0,columnspan=2 ,sticky='w',pady=20)
        ttk.Label(logframe, text='Email:',font = STDFONT, padding=5).grid(row=1,column=0,sticky='w',padx=15)
        ttk.Label(logframe, text='Contraseña:',font = STDFONT, padding=5).grid(row=3,column=0,sticky='w',padx=15)
        # dejo dos labels sin gridear para indicar contraseña y usario incorrectos
        self.pass_inco=ttk.Label(self.logframe, text='Contraseña Incorrecta',font = STDFONT, foreground='red',padding=5)
        self.user_inco=ttk.Label(self.logframe, text='Usuario no Registrado',font = STDFONT, foreground='red',padding=5)

        # variable del tkinter para recuperar la entrada de las entry (password y email)
        self.email = tk.StringVar()
        self.passw = tk.StringVar()

        name_entry=tk.Entry(logframe, textvariable = self.email, font=STDFONT,bd=0)
        name_entry.grid(row=2,column=0,sticky='w',padx=21,ipady=4)
        name_entry.focus_force()
        pass_entry=tk.Entry(logframe, textvariable = self.passw, show='*', font=STDFONT,bd=0)
        pass_entry.grid(row=4,column=0,sticky='w',padx=21,ipady=4)
        # para ejecutar la funcion de login al presionar enter en los cuadros de email o password
        pass_entry.bind('<Return>',lambda e: self.login()) 
        name_entry.bind('<Return>',lambda e: self.login()) 

        btn_login=ttk.Button(logframe, text="    INGRESAR    " ,padding=35, command=self.login ).grid(row=2,column=1, rowspan=3,sticky='w' )
        
        sep=ttk.Separator(logframe, orient='vertical')
        sep.grid(row=1,column=3,rowspan=5, sticky='ns')
        ttk.Label(logframe, text='CREAR NUEVA CUENTA',font = TITLE).grid(row=0,column=4,columnspan=2 )
        btn_reg=ttk.Button(logframe, text="  REGISTRARSE  " , command=self.llama_registro , style='flat.TButton',padding=35 ).grid(row=2,column=4,columnspan=2, rowspan=3)

        # Cartelera
        cartframe=tk.Frame(mainframe,bg=BACKGROUND)
        cartframe.grid(row=2,column=0,sticky ="nsew")
        cartframe.columnconfigure(0,weight=1)
        cartframe.columnconfigure(1,weight=1)
        cartframe.columnconfigure(2,weight=1)
        cartframe.columnconfigure(3,weight=1)
        cartframe.columnconfigure(4,weight=1)
        #cartframe['borderwidth'] = 5
        #cartframe['relief'] = 'groove'

        img1 = tk.PhotoImage(file="img\\image1.png",height=350)
        tk.Label(cartframe,image=img1).grid(row=0,column=0,padx=10)
        img2 = tk.PhotoImage(file="img\\image2.png",height=350)
        tk.Label(cartframe,image=img2).grid(row=0,column=1,padx=10)
        img3 = tk.PhotoImage(file="img\\image3.png",height=350)
        tk.Label(cartframe,image=img3).grid(row=0,column=2,padx=10)
        img4 = tk.PhotoImage(file="img\\image4.png",height=350)
        tk.Label(cartframe,image=img4).grid(row=0,column=3,padx=10)
        img5 = tk.PhotoImage(file="img\\image5.png",height=350)
        tk.Label(cartframe,image=img5).grid(row=0,column=4,padx=10)	


        self.mainloop() 


    def llama_registro(self):
        self.destroy()
        Registro()

    def login(self):
        self.pass_inco.grid_forget()   # Limpio las etiquetas de error del ingreso anterior 
        self.user_inco.grid_forget()
        mail=self.email.get()
        passw=self.passw.get()
        if mail!="" and passw!="":
            con=C_Usuarios()
            if con.esusuario(mail): # Verifico si el usuario existe en la base de datos segun su email
                val=con.validar(mail,passw)
                if  val!=None:       # Verifico si la contraseña es correcta y en ese caso  obtengo el id de usuario y sus permiso
                        if val[1]==0: # si tiene permisos 0 es un cliente
                            self.destroy()  #elimina la ventana 1 luego de recibir los datos
                            Cliente(val[0])
                        else:
                            self.destroy()  #elimina la ventana 1 luego de recibir los datos
                            Admin() 
                        
                else: # Contraseña incorrecta
                    self.pass_inco.grid(row=3,column=0,sticky='w',padx=15)
                    
            else:
                self.user_inco.grid(row=1,column=0,sticky='w',padx=15)
        else:
            messagebox.showinfo(message="Debe ingresar un usuario y una contraseña", title="Error")
        
 

        




Login()

