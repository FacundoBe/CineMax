import sqlite3 as sql

class Conexion_cinemark():

    def __init__(self):#bd es el nombre de la base de datos
        self.conexion = sql.connect('cinemark.db')
        self.cursor = self.conexion.cursor()

    def consulta(self, consulta):
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
        conexion.consulta('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER NOT NULL UNIQUE, nombre VARCHAR(20) NOT NULL, '
        + 'apellido VARCHAR(20) NOT NULL, email VARCHAR(255) NOT NULL ,password VARCHAR(20) NOT NULL, permisos INTEGER NOT NULL,' 
        + ' telefono INTEGER,  PRIMARY KEY (`id` AUTOINCREMENT)  ); ')
    
    def insertar(self,nombre,apellido,email,password,permisos,telefono=0):
        conexion=Conexion_cinemark()
        conexion.consulta(f' INSERT INTO usuarios (nombre, apellido, email, password,permisos, telefono) VALUES {nombre,apellido, email, password, permisos, telefono }')

    def esusuario(self,email): # Devuelve True si el email existe en la tabla usuarios
        conexion=Conexion_cinemark()
        res=conexion.consulta(f"SELECT email FROM usuarios WHERE email = '{email}'")
        return res.fetchone() != None

    def validar(self,email,password):
        conexion=Conexion_cinemark()
        res=conexion.consulta(f"SELECT id,permisos, password FROM usuarios WHERE email = '{email}'")
        data=res.fetchone()
        if data != None:            # Evita errores si el email no esta registrado.
            if data[2] == password:
                return  data[0],data[1]     # si la contraseña es correcta devuelve el ID del usuario, y sus permisos si no devuelve None



#user = C_Usuarios()
#user.insertar('facundo','javier','loe@gmail.com','contraseñasegura',0,4832554)
#print(user.validar('loe@gmail.com','contraseñasegura'))
