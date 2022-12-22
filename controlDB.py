import sqlite3 as sql
from datetime import datetime, timedelta
from settings import *

class Conexion_cinemark():

    def __init__(self):#bd es el nombre de la base de datos
        self.conexion = sql.connect(base_folder + '\\' + 'cinemark.db')
        self.cursor = self.conexion.cursor()
    
    def consultar(self, consulta):
       data= self.cursor.execute(consulta)
       self.commit()
       return data  
    
    def commit(self):
        self.conexion.commit()

    def close(self):
        self.conexion.close()


class C_Usuarios():
    def __init__(self):
        conexion = Conexion_cinemark()
        conexion.consultar('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER NOT NULL UNIQUE, nombre VARCHAR(20) NOT NULL, '
        + 'apellido VARCHAR(20) NOT NULL, email VARCHAR(255) NOT NULL ,password VARCHAR(20) NOT NULL, permisos INTEGER NOT NULL,' 
        + ' telefono INTEGER, descuento INTEGER, PRIMARY KEY (`id` AUTOINCREMENT)  ); ')
        conexion.close()
    
    def insertar(self,nombre,apellido,email,password,permisos,telefono=0):
        conexion=Conexion_cinemark()
        conexion.consultar(f' INSERT INTO usuarios (nombre, apellido, email, password,permisos, telefono, descuento) VALUES {nombre,apellido, email, password, permisos, telefono, 0} ')
        conexion.close

    def esusuario(self,email): # Devuelve True si el email existe en la tabla usuarios
        conexion=Conexion_cinemark()
        res=conexion.consultar(f"SELECT email FROM usuarios WHERE email = '{email}'")
        val=res.fetchone()
        conexion.close()
        return val != None
 
    def nombre(self,id): # Devuelve Tel nombre que corresponde a una id en particular
        conexion=Conexion_cinemark()
        res=conexion.consultar(f"SELECT nombre FROM usuarios WHERE id = {id}")
        nombre= res.fetchone() 
        if nombre != None:
            return nombre[0]
        conexion.close()
    
    def tiene_descuento(self,id): # Devuelve Tel nombre que corresponde a una id en particular
        conexion=Conexion_cinemark()
        res=conexion.consultar(f"SELECT descuento FROM usuarios WHERE id = {id}")
        descuento = res.fetchone() 
        conexion.close()
        return descuento[0]==1 #devuelve true si el valor es 1 y por ello tiene descuentos, en caso contrario no le corresponde
        
    def validar(self,email,password):
        conexion=Conexion_cinemark()
        res=conexion.consultar(f"SELECT id, permisos, password FROM usuarios WHERE email = '{email}'")
        data=res.fetchone()
        conexion.close()
        if data != None:            # Evita errores si el email no esta registrado.
            if data[2] == password:
                return  data[0],data[1]     # si la contraseña es correcta devuelve el ID del usuario, y sus permisos si no devuelve None
        



class C_Reservas():

    def __init__(self):
        conexion = Conexion_cinemark()
        conexion.consultar('CREATE TABLE IF NOT EXISTS "reservas" ( "idreservas"	INTEGER NOT NULL UNIQUE, "iduser"	INTEGER NOT NULL, 		'\
                          +'"idfuncion" INTEGER NOT NULL, "butacas"	INTEGER NOT NULL, 	"estado"	VARCHAR(10) NOT NULL, FOREIGN KEY("iduser") '\
	                      +'REFERENCES "usuarios"("id"), PRIMARY KEY("idreservas" AUTOINCREMENT) );')
        conexion.close()
    
    def insertar(self,iduser, idfuncion, butacas, estado):
        conexion=Conexion_cinemark()
        conexion.consultar(f' INSERT INTO reservas (iduser, idfuncion, butacas, estado) VALUES {iduser, idfuncion, butacas, estado}')
        conexion.close()

    def vencida(self,idfuncion):
        conex = Conexion_cinemark()
        conex.consultar(f'UPDATE reservas SET estado = "vencida" WHERE idfuncion = {idfuncion}')
        conex.close()

    def reservas_activas_por_cliente(self,id_cliente): #devuelve datos de todas las reservas para un cliente 
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT idreservas,idfuncion, butacas FROM "reservas" WHERE iduser = {id_cliente} AND estado = "activa" ')
        val = res.fetchall()
        conex.close()
        return val
    
    def eliminar_reserva(self, id:int):
        conex = Conexion_cinemark()
        conex.consultar(f"DELETE FROM reservas WHERE idreservas = {id}")
        conex.close()






class C_Salas():
    def __init__(self):
        conex = Conexion_cinemark()
        conex.consultar('CREATE TABLE IF NOT EXISTS "salas" ("idsalas"	INTEGER NOT NULL UNIQUE,"pelicula" TEXT NOT NULL,"sinopsis"	TEXT,"archivo_imagen" TEXT, "butacasmax"	INTEGER NOT NULL,"horarios"	TEXT NOT NULL, "fechalimite" TEXT NOT NULL, PRIMARY KEY("idsalas"));')
        conex.close()

    def crear_sala(self, id:int, pelicula:str,horarios:str, archivo_img:str, butacasmax:int,fechalimite,sinopsis=""):
        conex = Conexion_cinemark()
        conex.consultar(f"INSERT INTO Salas (idsalas, pelicula, sinopsis, archivo_imagen, butacasmax, horarios, fechalimite) VALUES { id, pelicula, sinopsis, archivo_img, butacasmax, horarios, fechalimite}")
        conex.close()
    
    def eliminar_sala(self, id:int):
        conex = Conexion_cinemark()
        conex.consultar(f"DELETE FROM Salas WHERE idsalas = {id}")
        conex.close()

    def datos_cartelera(self,): # Devuelve los datos necesarios para armar la cartelera
        conex = Conexion_cinemark()
        res=conex.consultar('SELECT idsalas, pelicula, archivo_imagen FROM "salas" ')
        val = res.fetchall()
        conex.close()
        return val

    def datos_funciones(self): # Devuelve los datos necesarios para armar las funciones
        conex = Conexion_cinemark()
        res=conex.consultar('SELECT idsalas, pelicula, horarios, butacasmax, fechalimite FROM "salas" ')
        val=res.fetchall()
        conex.close()
        return val
        
    def datos_completos(self,id): # Devuelve todos los datos de la sala
        conex = Conexion_cinemark()
        res = conex.consultar(f'SELECT * FROM "salas" WHERE idsalas = {id}')
        val = res.fetchone()
        conex.close()
        return val
    
    def butacasmax(self,id): # Devuelve el numero de butacas de la sala
        conex = Conexion_cinemark()
        res = conex.consultar(f'SELECT butacasmax FROM "salas" WHERE idsalas = {id}')
        val = res.fetchone()
        conex.close()
        return val[0]
        
    def datos_salas(self): # Devuelve los datos necesarios para mostrar salas/pelicula para eliminar
        conex = Conexion_cinemark()
        res=conex.consultar('SELECT idsalas, pelicula FROM "salas" ')
        val = res.fetchall()
        conex.close()
        return val
    
    def no_existe(self,id): # Devuelve true si la sala ya existe
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT idsalas FROM "salas" WHERE idsalas = {id}')
        val=res.fetchone()
        conex.close()
        return val == None
        



class C_Funciones():
    
    def __init__(self):
        conexion= Conexion_cinemark()
        conexion.consultar('CREATE TABLE IF NOT EXISTS "funciones" (	"idfuncion"	INTEGER NOT NULL UNIQUE, "idsalas"	INTEGER NOT NULL,'\
                           +'"dia" TEXT NOT NULL, "hora" TEXT NOT NULL,	"butacaslibres"	INTEGER NOT NULL,fechalimite TEXT,estado TEXT NOT NULL, PRIMARY KEY("idfuncion" AUTOINCREMENT));')
        conexion.close()

    def generar_funciones(self): # Genera las funciones de todas las salas atuales para los proximos 7 dias y la guarda en la base de datos
        con_salas=C_Salas()
        salas=con_salas.datos_funciones()
        salas=[list(x) for x in salas] # pasao cada sala de tupla  a lista
        for sala in salas: # Convierto los horarios en una lista de listas con formato [[HH, MM], [HH, MM], etc.  ]
            sala[2]=sala[2].split(',')
            sala[2]=[x.split(':') for x in sala[2]]
        ahora= datetime.now()
        for sala in salas:
            idsala=sala[0]
            fechalimite = datetime.strptime(sala[4], '%d/%m/%Y')
            butacasmax = sala[3]
            for delta_dia in range(0,7):
                dia_fun = ahora + timedelta(days=delta_dia) #Voy sumandole un dia mas a la fecha por ciclo
                if  fechalimite >= dia_fun: # verifica si la funcion esta dentro de la fecha limite (y si no no la crea)
                    for hora,minutos in sala[2]:
                        horario_funcion=datetime(dia_fun.year, dia_fun.month, dia_fun.day,int(hora),int(minutos))
                        dia_str= horario_funcion.strftime('%d/%m/%Y' )
                        hora_str= horario_funcion.strftime('%H:%M' )
                        if self.no_existe(idsala,dia_str, hora_str):    # Solo inserta la funcion si la misma no existe previamente como activa
                            self.crear_funcion(idsala, dia_str, hora_str,butacasmax)
    
    def no_existe(self, idsala, dia, hora):
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT idfuncion FROM "funciones" WHERE hora = "{hora}" AND dia = "{dia}" AND idsalas = {idsala}  ')
        val = res.fetchone()
        conex.close()
        return val == None
        
    def encontrar_id(self, idsala, dia, hora): #duvuelve le id de una funcion segun el horario y la sala correspondientes
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT idfuncion FROM "funciones" WHERE hora = "{hora}" AND dia = "{dia}" AND idsalas = {idsala}  ')
        val = res.fetchone()
        if val != None:
            return val[0]
        conex.close()
    
    def butacas_libres(self, idfuncion): #devuelve los asientos libres para una funcion
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT butacaslibres FROM "funciones" WHERE idfuncion = {idfuncion}  ')
        val = res.fetchone()[0]
        conex.close()
        return val
        
    def reservar_asiento(self, idfuncion, butacas_res):
        conex = Conexion_cinemark()
        conex.consultar(f'UPDATE funciones SET butacaslibres = butacaslibres - {butacas_res} WHERE idfuncion = {idfuncion}')
        conex.close()
    
    def crear_funcion(self, idsala,dia, hora, butacasmax):
        conex = Conexion_cinemark()
        conex.consultar(f'INSERT INTO funciones (idsalas, butacaslibres, dia, hora, estado) VALUES ({idsala}, {butacasmax}, "{dia}", "{hora}", "activa")')
        conex.close()
      
    def dia_y_hora(self, idsala): #devuelve una lista con los dias y las horas una pelicula considerando solo funcines activas
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT DISTINCT dia FROM "funciones" WHERE idsalas = {idsala} AND estado = "activa" ORDER BY dia ASC ')
        dias = res.fetchall()
        res=conex.consultar(f'SELECT DISTINCT hora FROM "funciones" WHERE idsalas = {idsala} AND estado = "activa" ORDER BY dia ASC ')
        horas = res.fetchall()
        conex.close()
        return dias,horas
    
    def vencida(self,idfuncion):
        conex = Conexion_cinemark()
        conex.consultar(f'UPDATE funciones SET estado = "vencida" WHERE idfuncion = {idfuncion}')
        conex.close()

    def func_activas(self): #devuelve una lista con todas las funciones que tienen estado = 'activa'
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT  idfuncion, dia, hora FROM "funciones" WHERE estado = "activa" ')
        func = res.fetchall()
        conex.close()
        return func
        
    def hay_vendidas(self, idsala): 
        """devuelve TRUE si existen funciones activas con asientos vendidos para la sala solicitada"""
        con_sal=C_Salas()
        butacasmax=con_sal.butacasmax(idsala)
        print(butacasmax)
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT idfuncion FROM "funciones" WHERE idsalas = {idsala} AND estado = "activa" AND butacaslibres < "{butacasmax}" ')
        val=res.fetchone()
        conex.close()
        return val !=None

    def datos_funcion(self,idfuncion):  
       conex = Conexion_cinemark()
       res=conex.consultar(f'SELECT  idsalas, dia, hora FROM "funciones" WHERE estado = "activa" AND idfuncion = {idfuncion} ')
       func = res.fetchall()
       if func != []:
            func=list(func[0])
       conex.close()
       return func



class C_Descuentos():
    
    def __init__(self):
        conexion= Conexion_cinemark()
        conexion.consultar('CREATE TABLE IF NOT EXISTS "descuentos" ("dia"	TEXT NOT NULL, descuento INTEGER, PRIMARY KEY("dia"));')
        conexion.close()
    
    def descuento(self,dias): # devuelve el descuento que le correspoonde a un dia ingresado por nombre ej. (martes) ojo los acentos
        conex = Conexion_cinemark()
        res=conex.consultar(f'SELECT descuento FROM descuentos WHERE dia = "{dias}" ')
        val = res.fetchone()[0]
        conex.close()
        return val
        




