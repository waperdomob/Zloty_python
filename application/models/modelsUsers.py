from flask import render_template, request, redirect, url_for, flash, session
from application.config.database import Database
from werkzeug.security import check_password_hash

class Users():

    db = Database()
    mysql = db.get_connection()

    def __init__(self):
        pass

    def get_users(self):
        conn = self.mysql.connect()
        cur= conn.cursor()
        cur.execute('''SELECT * FROM  gestionusuario''')
        data = cur.fetchall()
        conn.commit()
        return data
        
    def add_contacto(self,name,lastname,celphone,city,email,password_encrip):
        try:
            
            conn = self.mysql.connect()
            cur= conn.cursor()
            sql = 'INSERT INTO gestionusuario (nombre, apellido, telefono, ciudad, email, password) VALUES ( %s, %s, %s, %s, %s, %s)'
            data =  (name,lastname,celphone,city,email,password_encrip) #preparamos la consulta con el metodo execute del metodo con 
            cur.execute(sql,data)
            #self.mysql.connection.commit()
            conn.commit()
        except:
            print("Error 001 function add_contacto")

    def delete_contactos(self, id):
        try:
            conn = self.mysql.connection()
            cur= conn.cursor()
            sql = "DELETE FROM contactos WHERE id = {id}"
            cur.execute(sql.format(id = id))
            conn.commit()
            print(cur.rowcount, "record(s) deleted")
            return cur.rowcount
        except:
            print("Error 002 function delete_contacto")


    def get_by_id(self, id: int)-> tuple:
        try:
            cur = self.mysql.connection.cursor()
            sql = "SELECT * FROM contactos WHERE id = {id}"
            cur.execute(sql.format(id = id))
            data = cur.fetchall()
            return data
        except:
            print('Error function det_by_id')

            
    def update_contacto(self, id: int , nombre: str, telefono: int, email: str) -> int:
        try:
            cur = self.mysql.connection.cursor()
            sql = 'UPDATE contactos SET nombre = %s, telefono = %s, email = %s WHERE id = %s'
            values = (nombre, telefono, email, id)
            cur.execute(sql, values)
            self.mysql.connection.commit()
            print(cur.rowcount, "record(s) updated")
            return cur.rowcount
        except:
            print('Error function update_contacto')
            
    def verify_password(self, email, password_encrip1):
        conn = self.mysql.connect()
        cur= conn.cursor()
        cur.execute('''SELECT * FROM  gestionusuario WHERE email = %s''', email)
        data = cur.fetchone()
        conn.commit()
        if data:
            return check_password_hash(password_encrip1, data[6])
        else:
            flash('¡Usuario no encontrado!')
            return redirect(url_for('route_login')) 
