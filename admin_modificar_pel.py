import tkinter as tk
from tkinter import ttk
from settings import *
import utils.generic as utl
from tkinter import scrolledtext
from tkinter import filedialog
from controlDB import *
from tkinter import messagebox

class AdminModSala(tk.Toplevel):
    def __init__(self,id_sala):
        super().__init__()
        utl.centrar_ventana(self,1200,900)
        self.title('Modificar Película / Sala')
        self.resizable(0,0)
        self.iconbitmap(image_path+"\\favicon.ico")
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=3)
        self.columnconfigure(2,weight=1)
        
        self.id_sala= id_sala

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
        self.entry_titulo = tk.Entry(frame_izq, textvariable=self.titulo_entry, font=STDFONT,bd=0)
        self.entry_titulo.grid(row=1, ipady=5,padx=20,columnspan=5, sticky=tk.EW)
        
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
        self.entry_horario_1 = tk.Entry(frame_izq, textvariable=self.horario_entry_1, font=STDFONT,bd=0, width=4, justify="center")
        self.entry_horario_1.grid(row=5, column=0,ipadx=10, ipady=5, sticky="W", padx=(20,1))
        
        self.horario_entry_2 = tk.StringVar()
        self.entry_horario_2 = tk.Entry(frame_izq, textvariable=self.horario_entry_2, font=STDFONT,bd=0, width=4, justify="center")
        self.entry_horario_2.grid(row=5, column=1,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_3 = tk.StringVar()
        self.entry_horario_3 = tk.Entry(frame_izq, textvariable=self.horario_entry_3, font=STDFONT,bd=0, width=4, justify="center")
        self.entry_horario_3.grid(row=5, column=2,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_4 = tk.StringVar()
        self.entry_horario_4 = tk.Entry(frame_izq, textvariable=self.horario_entry_4, font=STDFONT,bd=0, width=4, justify="center")
        self.entry_horario_4.grid(row=5, column=3,ipadx=10, ipady=5, sticky="W",padx=1)
        
        self.horario_entry_5 = tk.StringVar()
        self.entry_horario_5 = tk.Entry(frame_izq, textvariable=self.horario_entry_5, font=STDFONT,bd=0, width=4, justify="center")
        self.entry_horario_5.grid(row=5, column=4,ipadx=10, ipady=5, sticky="W",padx=1)
        
        #Selector numero de Sala
        label_entry_sala = tk.Label(frame_izq, text=f"  Sala ", font=STDFONT)
        label_entry_sala.grid(row=4,column=5, padx=(20), sticky="W", pady=(30,0))
        
        self.sala_elegida = tk.StringVar(value=0)
        spinbox_salas = ttk.Spinbox(frame_izq,from_=1,to=5,textvariable=self.sala_elegida,wrap=True,justify="center",width=4,font=STDFONT)
        spinbox_salas.grid(row=5, column=5,sticky="W",padx=16)
        spinbox_salas.set(self.id_sala)
        spinbox_salas.configure(state='disabled')
        
        #Selector de cantidad maxima de asientos
        label_entry_butacasmax = tk.Label(frame_izq, text="MaxButacas", font=STDFONT)
        label_entry_butacasmax.grid(row=4,column=6,sticky="W", pady=(30,0), columnspan=2)
        
        self.butacasmax = tk.StringVar(value=0)
        self.spinbox_butacasmax = ttk.Spinbox(frame_izq,from_=1,to=99,textvariable=self.butacasmax,wrap=True,justify="center",width=6,font=STDFONT)
        self.spinbox_butacasmax.grid(row=5, column=6,sticky="N")
        self.spinbox_butacasmax.set(1)
        
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

        self.carga_sala(self.id_sala) #Inicializa los wigets con los datos de la sala a modificar

        

    def carga_sala(self,id):
        """ Cargo los datos de la sala en los wigets del tkinter"""
        conex_salas= C_Salas()
        sala = conex_salas.datos_completos(id)
        pelicula=sala[1]
        sinopsis=sala[2]
        archivo=sala[3]
        butacasmax=sala[4]
        horarios=sala[5].split(',')
        fechalimite=sala[6]
        self.entry_titulo.insert(0,pelicula)
        self.entry_sinopsis.insert('1.0',sinopsis)
        self.entry_venc.delete(0, "end") # borra todo el texto del entry
        self.entry_venc.insert(0, fechalimite)
        self.entry_img.insert(0,archivo) 
        self.spinbox_butacasmax.set(butacasmax)

        for ind,horario in enumerate(horarios):
            if ind ==0:
                self.entry_horario_1.insert(0,horario)
            if ind==1:
                self.entry_horario_2.insert(0,horario)
            if ind==2:
                self.entry_horario_3.insert(0,horario)
            if ind==3:
                self.entry_horario_4.insert(0,horario)
            if ind==4:
                self.entry_horario_5.insert(0,horario)


    def guardar(self):
        self.venc=self.venc_entry.get()
        self.butacas = self.butacasmax.get()
        self.sinopsis =  self.entry_sinopsis.get("1.0", "end-1c")
        self.titulo = self.titulo_entry.get()
        self.archivo=self.imgpel_entry.get()
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
                    conex_sala.modificar_sala(sala,self.titulo, horarios, self.archivo, self.butacas, self.venc, self.sinopsis)
                    self.destroy()
                  
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
