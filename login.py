import tkinter as tk
from tkinter import ttk
from controlDB import C_Usuarios
import utils.generic as utl
from admin import Admin
from cliente import Cliente



# Colores
MAINBAR =("Verdana", 24, 'bold')
TITLE = ("Verdana", 16)
STDFONT=("Verdana", 12)
DARKCOLOR='#151537'
BUTTONCOL='#2d7086'
BUTTONHOV='#19404d'
BUTTONPRESS='#398fac'
BACKGROUND='#e3e5e8'


class Login(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry('1200x900')
        self.title('LOGIN')
        utl.centrar_ventana(self,1200,900)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        #mainframe.columnconfigure(1, weight=1)
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

        # Marco del login
        logframe=tk.Frame(mainframe,bg=BACKGROUND)
        self.logframe=logframe                      #Guardo uan rfeecina al marco de login/registro
        logframe.columnconfigure(0,weight=2)
        logframe.columnconfigure(1,weight=2)
        logframe.columnconfigure(3,weight=1)
        logframe.columnconfigure(4,weight=2)
        logframe.columnconfigure(5,weight=2)
        logframe.grid(row=1,column=0,sticky ="nsew",padx=100,pady=15)
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
        tk.Entry(logframe, textvariable = self.passw, show='*', font=STDFONT,bd=0).grid(row=4,column=0,sticky='w',padx=21,ipady=4)
        

        btn_login=ttk.Button(logframe, text="    INGRESAR    " ,padding=35, command=self.login ).grid(row=2,column=1, rowspan=3,sticky='w' )

        sep=ttk.Separator(logframe, orient='vertical')
        sep.grid(row=1,column=3,rowspan=4, sticky='ns')
        ttk.Label(logframe, text='CREAR NUEVA CUENTA',font = TITLE).grid(row=0,column=4,columnspan=2 )
        btn_reg=ttk.Button(logframe, text="  REGISTRARSE  " , style='flat.TButton',padding=35).grid(row=2,column=4,columnspan=2, rowspan=3)

    def login(self):
        self.pass_inco.grid_forget()   # Limpio las etiquetas de error del ingreso anterior 
        self.user_inco.grid_forget()
        mail=self.email.get()
        passw=self.passw.get()
        print(mail,passw)
        con=C_Usuarios()
        if con.esusuario(mail): # Verifico si el usuario existe en la base de datos segun su email
            val=con.validar(mail,passw)
            print(val) 
            if  val!=None:       # Verifico si la contraseña es correcta y en ese caso  obtengo el id de usuario y sus permiso
                    if val[1]==0: # si tiene permisos 0 es un cliente
                        Cliente()
                    else:
                        Admin() 
                    self.destroy()  #elimina la ventana 1 luego de recibir los datos
            else: # Contraseña incorrecta
                self.pass_inco.grid(row=3,column=0,sticky='w',padx=15)
                
        else:
            self.user_inco.grid(row=1,column=0,sticky='w',padx=15)
        
 

        




l=Login()
l.mainloop()
