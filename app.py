from flask import Flask,render_template,redirect,request,url_for,flash
import mysql.connector

#creamos una instacia de la clase flask
app = Flask(__name__)

#definir ruta
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2025"
)

cursor = db.cursor()

#definir ruta
@app.route('/')
def lista():#item
    cursor= db.cursor()
    cursor.execute('select * FROM emple')
    usuario = cursor.fetchall()

    return render_template('index.html',emple=usuario)#esta renderizando el index.html

@app.route('/Registrar', methods=['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
       Nombres = request.form.get('NOMBRE')
       apellidos= request.form.get('APELLIDO')
       correos= request.form.get('CORREO')
       telefonos= request.form.get('TELEFONO')
       direcciones= request.form.get('DIRECION')
       usuarios= request.form.get('USUARIO')
       contrasenas= request.form.get('CONTRASENA')
#insertar datis a la tabla personas 
    
       cursor.execute("INSERT INTO emple(nombre ,apellido,correo ,direccion ,telefono ,usuario ,contrasena )VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombres,apellidos,correos,direcciones,telefonos,usuarios,contrasenas))
       db.commit()
#redirigir a la misma pagina cuando el metodo es post
       return redirect(url_for('registrar_usuario'))
#si es un metodo 
    return render_template('Registrar.html')
#definir rutas

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_usuario(id):
    cursor =db.cursor()
    if request.method  == 'POST':
       nombres = request.form.get('nombre')
       apellidos = request.form.get('apellido')
       email = request.form.get('correo')
       dire = request.form.get('direccion')
       tel = request.form.get('telefono')
       usuarios = request.form.get('usuario')
       password = request.form.get('contrasena')

        #sentencia para actualizar los datos en la base de datos
       sql = "UPDATE emple SET nombre=%s, apellido=%s, correo=%s, direccion=%s, telefono=%s, usuario=%s, contrasena=%s WHERE identificacionperso=%s"
       cursor.execute(sql, (nombres,apellidos,email,dire,tel,usuarios,password,id))
       db.commit()
       return redirect(url_for('lista'))#redirecciona a una url
    else:
        cursor=db.cursor()
        #obtener los datos de la persona que se va a editar
        cursor.execute('SELECT * FROM emple WHERE identificacionperso = %s', (id,))
        data = cursor.fetchall()
    if data:
        return render_template('editar.html',emple=data[0])
    else:
        flash('usuario no encontrado','error')
        return redirect(url_for('lista'))

       
@app.route('/eliminar/<int:id>',methods=['GET','POST'])
def eliminar_usuario(id):
    cursor =db.cursor()
    if request.method =='POST':
       cursor.execute( 'DELETE FROM emple WHERE identificacionperso =%s',(id,)  ) 
       db.commit()   
       return redirect (url_for('lista'))
    else:
        cursor.execute('SELECT* FROM emple WHERE identificacionperso=%s',(id,) )
        data = cursor.fetchall()
        if data:
           return render_template('eliminar.html',emple=data)


#para ejecutar instalacion 


#para ejecutar la aplicacion 
if __name__== '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)
    