import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from settings import *
from controlDB import C_Usuarios, C_Salas
import utils.generic as utl
from admin import Admin
from cliente import Cliente
from registro import Registro


class Login(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry('1200x900')
        self.title('LOGIN')
        self.iconbitmap(image_path+'/favicon.ico')
        utl.centrar_ventana(self,1200,900)
        # Creo el marco principal
        mainframe=tk.Frame(self,background=BACKGROUND)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=2)
        mainframe.rowconfigure(1,weight=20)
        mainframe.rowconfigure(2,weight=10)
        mainframe.pack(side="left", expand=tk.YES, fill=tk.BOTH)  

        # Faja superior
        topframe = tk.Frame(mainframe, bg=DARKCOLOR, width=1200, height=80)
        topframe.grid(row=0, sticky="ew")
        topframe.grid_columnconfigure(0, weight=1)
        topframe.grid_rowconfigure(0, weight=1)
        topframe.grid_propagate(False)
        encabezado_izq = tk.Label(topframe, text="CINEMARK", background=DARKCOLOR, fg="white", font=MAINBAR)
        encabezado_izq.grid(row=0,padx=20, sticky=tk.W)

        # Marco del login
        logframe=tk.Frame(mainframe,bg=BACKGROUND)
        self.logframe=logframe                      # Guardo una referencia al marco de login/registro Lo uso para modificar los
        logframe.columnconfigure(0,weight=2)        # labels de contraseña y email erroneos 
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
        s.configure('grey.TLabel', background=BACKGROUND, foreground=BUTTONPRESS)

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
        
        olvido_passw=ttk.Label(logframe, text='Olvido su Contraseña?',font = SMALLFONT,style='grey.TLabel', padding=5)
        olvido_passw.grid(row=5,column=0,sticky='w',padx=15)
        olvido_passw.bind('<Button-1>',lambda e: messagebox.showinfo(message="Funcionalidad disponible en Breve", title="En construccion"))
        btn_login=ttk.Button(logframe, text="    INGRESAR    " ,padding=35, command=self.login ).grid(row=2,column=1, rowspan=3,sticky='w' )
        

        sep=ttk.Separator(logframe, orient='vertical')
        sep.grid(row=1,column=3,rowspan=5, sticky='ns')
        ttk.Label(logframe, text='CREAR NUEVA CUENTA',font = TITLE).grid(row=0,column=4,columnspan=2 )
        btn_reg=ttk.Button(logframe, text="  REGISTRARSE  " , command=self.llama_registro , style='flat.TButton',padding=35 ).grid(row=2,column=4,columnspan=2, rowspan=3)

        # Cartelera
        cartframe=tk.Frame(mainframe,bg=BACKGROUND)
        cartframe.grid(row=2,column=0,sticky ="nsew")
        for i in range(5) : cartframe.columnconfigure(i,weight=1) #creo 5 columnas iguales
 
       
        salas=C_Salas() # Leo las peliculas en cartelera
        peliculas=salas.datos_cartelera()
        
        
        self.img = {}

        HEIGTH=342 # setea la altura del label (deberia ser igual a la altura de la imagen de la pelicula )
        for ind,peli in enumerate(peliculas):

            self.img[ind] = tk.PhotoImage(file= image_path +'\\' + peli[2], height=HEIGTH)
            tk.Label(cartframe,image=self.img[ind]).grid(row=0,column=ind,padx=10)           
            ttk.Label(cartframe, text=f'{peli[1]}',font = TITLE).grid(row=1,column=ind,pady=5)    
            ttk.Label(cartframe, text=f'SALA {peli[0]}',font = TITLEBOLD).grid(row=3,column=ind,pady=5)    


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
            messagebox.showwarning(message="Debe ingresar un usuario y una contraseña", title="Error")
        
 

if __name__ == '__main__':   
    Login()

