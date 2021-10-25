from pymysql import NULL
from application import app
from flask import Flask, jsonify    #importamos los modulos necesarios
from flask import render_template, request, redirect, url_for, flash, session
from application.models.modelsUsers import Users
from application.config.database import Database
from werkzeug.security import generate_password_hash as genph
from werkzeug.security import check_password_hash as checkph




db = Database()
ModelUser = Users()
#route index
@app.route('/')
def index():
    return render_template('/frms/index.html')

@app.route('/index_user')
def index_user():
    if 'email' in session:
        id_user = session['id']
        print (id_user)
        return render_template('/frms/index_user.html',id = id_user)
    else:
        flash('¡Debes estar logueado!')
        return redirect(url_for('route_login'))

@app.route('/sign_up')
def sign_up():
    return render_template('/frms/Sign_up.html')

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        try:
            name = request.form['nombre']
            lastname = request.form['apellido']
            celphone= request.form['telefono']            
            city = request.form['ciudad']
            _email = request.form['correo']
            password = request.form['password_']            
            passwordConfir = request.form['confirpassword']     
            if password == passwordConfir:
                    
                    password_encrip = genph(password)        
                    ModelUser.add_contacto(name, lastname,celphone, city, _email, password_encrip)
                    return redirect('/')
            else:                          
                    
                    flash('La contraseña no coincide')
                    return redirect(url_for('sign_up'))
        except:
            flash('¡Ah ocurrido un error!')
            return redirect(url_for('sign_up'))#redireciona al mismo formulario    
            
@app.route('/route_login')
def route_login():
    return render_template('/frms/login.html')            

@app.route('/login', methods=['POST'])
def login():
     if request.method == 'POST':
                   
            email = request.form['email_']
            password = request.form['password_']
            
            conn = db.mysql.connect()
            cur= conn.cursor()
            sql = "SELECT * FROM gestionusuario WHERE email = %s "
            cur.execute(sql,email)
            data = cur.fetchone()                        
            conn.commit()
                       
            if data :
                
                if checkph(data[6],password):
                    flash('Bienvenido '+email)
                    session['id'] = data[0]
                    session['name'] = data[1]
                    session['email'] = email
                    return redirect(url_for('index_user'))
                else:
                    flash('¡Usuario o contraseña incorrecta!')
                    return redirect(url_for('route_login'))
            else:
                flash('¡Usuario no encontrado!')
                return redirect(url_for('route_login'))            

@app.route('/edit_user/<id>')
def edit_user(id):
      
    conn = db.mysql.connect()
    cur= conn.cursor()
    cur.execute("SELECT * FROM `gestionusuario` ")
    empleados = cur.fetchall()
    conn.commit() 
    
    return render_template('/frms/team.html')


@app.route("/log_out")
def log_out():
    if 'email' in session:
        session.pop('email')
        return redirect(url_for('index'))  

@app.route('/team')
def team():
    return render_template('/frms/team.html')