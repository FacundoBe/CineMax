import sqlite3 as sql


class Conexion_cinemark():

    def __init__(self):#bd es el nombre de la base de datos
        self.conexion = sql.connect('cinemark.db')
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
        + ' telefono INTEGER,  PRIMARY KEY (`id` AUTOINCREMENT)  ); ')
        conexion.close()
    
    def insertar(self,nombre,apellido,email,password,permisos,telefono=0):
        conexion=Conexion_cinemark()
        conexion.consultar(f' INSERT INTO usuarios (nombre, apellido, email, password,permisos, telefono) VALUES {nombre,apellido, email, password, permisos, telefono }')
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

    def validar(self,email,password):
        conexion=Conexion_cinemark()
        res=conexion.consultar(f"SELECT id, permisos, password FROM usuarios WHERE email = '{email}'")
        data=res.fetchone()
        if data != None:            # Evita errores si el email no esta registrado.
            if data[2] == password:
                return  data[0],data[1]     # si la contraseña es correcta devuelve el ID del usuario, y sus permisos si no devuelve None
        conexion.close()



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



class C_Salas():
    def __init__(self):
        conex = Conexion_cinemark()
        conex.consultar('CREATE TABLE IF NOT EXISTS "salas" ("idsalas"	INTEGER NOT NULL UNIQUE,"pelicula" TEXT NOT NULL,"sinopsis"	TEXT,"archivo_imagen" TEXT, "butacasmax"	INTEGER NOT NULL,"horarios"	TEXT NOT NULL,PRIMARY KEY("idsalas"));')
        conex.close()

    def crear_sala(self, id:int, pelicula:str,horarios:str, archivo_img:str, butacasmax:int, sinopsis=""):
        conex = Conexion_cinemark()
        conex.consultar(f"INSERT INTO Salas (idsalas, pelicula, sinopsis, archivo_imagen, butacasmax, horarios) VALUES { id, pelicula, sinopsis, archivo_img, butacasmax, horarios}")
        conex.close()
    
    def eliminar_sala(self, id:int):
        conex = Conexion_cinemark()
        conex.consultar(f"DELETE FROM Salas WHERE idsalas = {id}")
        conex.close()

    def datos_cartelera(self,): # Devuelve los datos necesarios para armar la cartelera
        conex = Conexion_cinemark()
        res=conex.consultar('SELECT idsalas, pelicula, archivo_imagen FROM "salas" ')
        return res.fetchall()
        conex.close()
    




class C_Funciones():
    
    def __init__(self):
        conexion= Conexion_cinemark()
        conexion.consultar('CREATE TABLE "funciones" (	"idfuncion"	INTEGER NOT NULL UNIQUE, "idsalas"	INTEGER NOT NULL,'\
                           +'"dia"	TEXT NOT NULL,	"hora"	TEXT NOT NULL,	"butacaslibres"	INTEGER NOT NULL, PRIMARY KEY("idfuncion" AUTOINCREMENT));')
        conexion.close()


#c = C_Reservas()
#c.insertar(1,1,3,'Activa' )
sala1= C_Salas()
print(sala1.datos_cartelera())
#sala1.crear_sala(2, "Historia de Honor", "19:30, 21:30", "image2.png",45, " muy fea pelicula no ver en familia no vale la pena" )
