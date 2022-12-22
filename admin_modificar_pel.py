import tkinter as tk
from tkinter import ttk
from settings import *
import utils.generic as utl
from tkinter import scrolledtext
from tkinter import filedialog
from controlDB import *
from tkinter import messagebox

class AdminModSala(tk.Toplevel):
    def __init__(self):
        super().__init__()
        utl.centrar_ventana(self,1200,900)
        self.title('Modificar Película / Sala')
        self.resizable(0,0)
        self.iconbitmap("img\\favicon.ico")
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=3)
        self.columnconfigure(2,weight=1)

        #Estilo 
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('TButton', relief='flat' ,font = STDFONT, foreground="white", background=BUTTONCOL )
        s.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')], background=[('pressed', BUTTONPRESS ),('disabled','grey' ), ('active', BUTTONHOV)])
        #s.configure('TLabel', relief='flat' , background=BACKGROUND )
        s.configure('grey.TButton', relief='flat' ,font = TITLE, foreground=BACKGROUND, background=BUTTONCLEAR )
        s.configure('cancel.TButton', relief='flat' ,font = STDFONT, foreground="white", background=REDBUTTON )
        s.configure('grey.TLabel', background=BACKGROUND, foreground=BUTTONPRESS)
        s.configure('TRadiobutton', font = TITLE,  background=BACKGROUND )
        s.configure('TSpinbox', font = TITLE, arrowsize=14 )

        
        
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
        
        # titulo de pagina
        frame_titulo = tk.Frame(self, width=700, height=120)
        frame_titulo.grid(row=1,column=1, sticky="N")
        frame_titulo.grid_columnconfigure(0, weight=1)
        frame_titulo.grid_rowconfigure(0, weight=1)
        frame_titulo.grid_propagate(False)
        titulo_label = tk.Label(frame_titulo, text="Modificar Película / Sala", fg="gray", font=("Verdana", 22))
        titulo_label.grid(row=0,padx=20, sticky="N", pady=(50,10))

         #separador central / superior
        sep_inf=ttk.Separator(frame_titulo, orient='horizontal')
        sep_inf.grid(row=1,column=0, sticky='WE',padx=(20,10))
        
        #Seccion Central
        frame_izq = tk.Frame(self, width=700, height=600)
        frame_izq.grid(row=2,column=1, sticky="N", pady=30)
        frame_izq.grid_propagate(False)
        
        for i in range(7) : frame_izq.grid_columnconfigure(i,weight=1) #Creo 7 columnas iguales dentro del Frame izq
        
        #Entrada de datos para ingresar titulo de la pelicula
        label_entry_titulo = tk.Label(frame_izq, text="Título de la Película", font=STDFONT)
        label_entry_titulo.grid(row=0,column=0, padx=20, sticky="w", pady=(5,10), columnspan=4)
        
        self.titulo = ""
        self.titulo_entry = tk.StringVar()
        entry_titulo = tk.Entry(frame_izq, textvariable=self.titulo_entry, font=STDFONT,bd=0)
        entry_titulo.grid(row=1, ipady=5,padx=20,columnspan=5, sticky=tk.EW)
        
        #Entrada de datos para ingresar fecha de finalizacion de funciones
        label_entry_titulo = tk.Label(frame_izq, text="Funciones hasta:", font=SMALLFONT)
        label_entry_titulo.grid(row=0,column=5, sticky="N", pady=(30,10), columnspan=4)
        
        self.venc = ""
        self.venc_entry = tk.StringVar()
        self.entry_venc = tk.Entry(frame_izq, textvariable=self.venc_entry, font=STDFONT,bd=0,width=20, justify="center")
        self.entry_venc.grid(row=1,column=5, ipady=5,padx=20,columnspan=3)
        
        self.entry_venc.insert(0, 'dd/mm/aaaa')
        self.entry_venc.bind('<FocusIn>', self.entry_click)
        self.entry_venc.bind('<FocusOut>', self.focusout)
        self.entry_venc.config(fg = 'grey')
 
        
        #Entrada de datos para ingresar la sinopsis de la pelicula
        label_entry_sinopsis = tk.Label(frame_izq, text="Sinopsis", font=STDFONT)
        label_entry_sinopsis.grid(row=2,column=0, padx=20, sticky="w", pady=(30,10), columnspan=6)
        
        self.sinopsis = ""
        self.entry_sinopsis = scrolledtext.ScrolledText(frame_izq,wrap=tk.WORD, height=8, font=STDFONT,bd=0)
        self.entry_sinopsis.grid(row=3,padx=20, columnspan=7)

        #seccion horarios de la funcion
        label_horarios = tk.Label(frame_izq, text="Horarios de la Función (hh:mm)", font=STDFONT)
        label_horarios.grid(row=4,column=0, padx=20, sticky="w", pady=(30,10), columnspan=5)  
        
        self.horarios=""
        self.horario_entry_1 = tk.StringVar()
        entry_horario_1 = tk.Entry(frame_izq, textvariable=self.horario_entry_1, font=STDFONT,bd=0, width=4, justify="center")
        entry_horario_1.grid(row=5, column=0,ipadx=10, ipady=5, sticky="W", padx=(20,1))
        
        self.horario_entry_2 = tk.StringVar()
        entry_horario_2 = tk.Entry(frame_izq, textvariable=self.horario_entry_2, font=STDFONT,bd=0, width=4, justify="center")
        entry_horario_2.grid(row=5, column=1,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_3 = tk.StringVar()
        entry_horario_3 = tk.Entry(frame_izq, textvariable=self.horario_entry_3, font=STDFONT,bd=0, width=4, justify="center")
        entry_horario_3.grid(row=5, column=2,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_4 = tk.StringVar()
        entry_horario_4 = tk.Entry(frame_izq, textvariable=self.horario_entry_4, font=STDFONT,bd=0, width=4, justify="center")
        entry_horario_4.grid(row=5, column=3,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_5 = tk.StringVar()
        entry_horario_5 = tk.Entry(frame_izq, textvariable=self.horario_entry_5, font=STDFONT,bd=0, width=4, justify="center")
        entry_horario_5.grid(row=5, column=4,ipadx=10, ipady=5, sticky="W",padx=1)
        
        #Selector numero de Sala
        label_entry_sala = tk.Label(frame_izq, text="  Sala", font=STDFONT)
        label_entry_sala.grid(row=4,column=5, padx=(20), sticky="W", pady=(30,0))
        
        self.sala_elegida = tk.StringVar(value=0)
        spinbox_salas = ttk.Spinbox(frame_izq,from_=1,to=5,textvariable=self.sala_elegida,wrap=True,justify="center",width=4,font=STDFONT)
        spinbox_salas.grid(row=5, column=5,sticky="W",padx=16)
        spinbox_salas.set(1)
        
        #Selector de cantidad maxima de asientos
        label_entry_butacasmax = tk.Label(frame_izq, text="MaxButacas", font=STDFONT)
        label_entry_butacasmax.grid(row=4,column=6,sticky="W", pady=(30,0), columnspan=2)
        
        self.butacasmax = tk.StringVar(value=0)
        spinbox_butacasmax = ttk.Spinbox(frame_izq,from_=1,to=99,textvariable=self.butacasmax,wrap=True,justify="center",width=6,font=STDFONT)
        spinbox_butacasmax.grid(row=5, column=6,sticky="N")
        spinbox_butacasmax.set(1)
        
        #Entrada de datos para seleccionar imagen de pelicula
        label_entry_img = tk.Label(frame_izq, text="Archivo de carátula", font=STDFONT)
        label_entry_img.grid(row=6,column=0, padx=20, sticky="w", pady=(30,0), columnspan=3)

        btn_buscar_imgpel=ttk.Button(frame_izq, text="Explorar" , command=self.explorar, style='flat.TButton',width=20).grid(row=6,column=2, pady=(40,7),padx=10,sticky='E',columnspan=2)

        self.imgpel_entry = tk.StringVar()
        self.entry_img = tk.Entry(frame_izq, textvariable=self.imgpel_entry, font=STDFONT,bd=0)
        self.entry_img.grid(row=7, ipady=(5),padx=(20,10),columnspan=4, sticky=tk.EW)
        
        btn_aPelicula=ttk.Button(frame_izq, text="Modificar Pelicula " , command=self.guardar, style='flat.TButton',padding=20, width=30).grid(row=6,column=4, pady=(40,7),padx=10,sticky='WE', rowspan=2,columnspan=3)

        #separador central / inferior
        sep_inf=ttk.Separator(frame_izq, orient='horizontal')
        sep_inf.grid(row=9,column=0,columnspan=7, sticky='WE', pady=35, padx=(20,10))

        
        self.mainloop()

    def actualiza_salas(self):
        # Cargo la lista de salas de la base de datos
        conex_salas= C_Salas()
        self.lista_salas = conex_salas.datos_salas()
        sala_string = []
        for sala in self.lista_salas:
            sala_string.append(f" Sala {sala[0]} : {sala[1]}") # armo un string por sala
        
        list_peliculas = tk.Variable(value=sala_string)
        self.lb_pelis.config(listvariable=list_peliculas)
        

    def guardar(self):
        self.butacas = self.butacasmax.get()
        self.sinopsis =  self.entry_sinopsis.get("1.0", "end-1c")
        self.titulo = self.titulo_entry.get()
        if self.imgpel_entry != "":
            if self.titulo !="":
                hor1 = self.horario_entry_1.get()
                hor2 = self.horario_entry_2.get()
                hor3 = self.horario_entry_3.get()
                hor4 = self.horario_entry_4.get()
                hor5 = self.horario_entry_5.get()
                horarios = [hor1,hor2,hor3,hor4,hor5]
                horarios = [x for x in horarios if x !=""]
                if len(horarios) > 0 :
                    horarios = ",".join(horarios) 
                    sala = int(self.sala_elegida.get())
                   
                    conex_sala = C_Salas()
                    if conex_sala.no_existe(sala): #solo escribe la sala si no existe una con el mismo id
                        conex_sala.crear_sala(sala,self.titulo, horarios, self.imgpel_entry,self.butacas, self.sinopsis)
                        self.actualiza_salas()# actualiza la lista de salas con las sala recien creada
                    else:
                        messagebox.showwarning(message="La sala ya existe", title="Error")

                else: #Corresponde al if de horarios
                    messagebox.showwarning(message="Debe tener como mínimo un horario", title="Error")

            else:
                messagebox.showwarning(message="Debe escribir un titulo", title="Error")

        else:
           messagebox.showwarning(message="Debe elegir una imagen", title="Error")
             
    
    def explorar(self):
        filename =filedialog.askopenfilename(initialdir= image_path, filetypes=(("png files","*.png"),("jpg files","*.jpg"),("tiff files","*.tiff"),("All files","*.*")))
        filename = filename.split("/")[-1]
        self.imgpel_entry = filename
        self.entry_img.insert(tk.END, filename)

    def guardar_desc(self):
        pass

    def eliminar_sala(self):
        index = self.lb_pelis.curselection()
        if (len(index)==0):
            return
        indice = index[0]
        id = self.lista_salas[indice][0]
        
        conex_funcion = C_Funciones()
        if conex_funcion.hay_activas(id) == False:
            self.lb_pelis.delete(indice) # Esto elimina la sala de la ventana listbox, no de la base de datos
            conex_salas = C_Salas()
            conex_salas.eliminar_sala(id)   #elimina la sala elegida de la Base de datos
        else:
            messagebox.showwarning(message=f"No se puede eliminar la Sala {id} porque tiene funciones activas", title="Error")


    def entry_click(self,event):
        """Funcion que se llama cuando se le hace click al entry"""
        if self.entry_venc.get() == 'dd/mm/aaaa':
            self.entry_venc.delete(0, "end") # borra todo el texto del entry
            self.entry_venc.insert(0, '') #Inserta espacio en blanco para que se puedan ingresar los datos
            self.entry_venc.config(fg = 'black')
    
    def focusout(self,event):
        if self.entry_venc.get() == '':
            self.entry_venc.insert(0, 'dd/mm/aaaa')
            self.entry_venc.config(fg = 'grey')
