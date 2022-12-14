from datetime import datetime
from settings import *


def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):    
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (aplicacion_ancho/2))
    y = int((pantall_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

def nombre_dias(dia): # devuelve el nombre del dia para una fecha en formato '%d/%m/%Y'
    diaDT=datetime.strptime(dia , '%d/%m/%Y')
    return diaDT.strftime('%A')
