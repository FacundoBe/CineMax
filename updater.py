from controlDB import *
from datetime import datetime


def actualizar_vencidas_BD(): # Encuentra las funciones y reservas que en este momento ya pasaron y actualiza el estado a vencida en la BD
    fun=C_Funciones()
    funciones=fun.func_activas()
    for funcion in funciones:
        horario_str=f'{funcion[1]} {funcion[2]}'
        horario_datetime=datetime.strptime( horario_str, '%d/%m/%Y %H:%M') # convierto el horario de str a objeto datetime
        if horario_datetime < datetime.now(): #si la reserva corresponde a una fecha que ya paso cambio su estado a vencida
            fun.vencida(funcion[0]) # actualiza las funciones
            res=C_Reservas()
            res.vencida(funcion[0]) # actualiza las Reservas

