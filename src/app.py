from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movies'

UPLOADS = os.path.join('uploads/')
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM movie;"
    cursor.execute(sql)

    movies = cursor.fetchall()

    conn.commit()

    return render_template('movies/index.html', movies = movies)

@app.route('/create')
def create():
    return render_template('movies/create.html')

@app.route('/store', methods=['POST'])
def store():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtDesc']
    _genero = request.form['txtGene']
    _imagen = request.files['txtImg']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _imagen.filename != '':
        nuevoNombreImagen = tiempo + '_' + _imagen.filename
        _imagen.save('uploads/' + nuevoNombreImagen)

    sql = "INSERT INTO movie (nombre,descripcion,genero,image) values(%s, %s, %s, %s);"
    datos = (_nombre,_descripcion,_genero,nuevoNombreImagen)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM movie WHERE id=%s"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,id)
    conn.commit()

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM movie WHERE id=%s"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,id)
    movie = cursor.fetchone()

    conn.commit()

    return render_template('movies/edit.html', movie=movie)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtDesc']
    _genero = request.form['txtGene']
    _imagen = request.files['txtImg']
    id = request.form['txtId']

    datos = (_nombre, _descripcion, _genero, id)

    print(datos)

    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "SELECT image FROM movie WHERE id=%s"
    cursor.execute(sql, id)

    nombreFoto = cursor.fetchone()[0]

    if _imagen.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreImagen = tiempo + '_' + _imagen.filename
        _imagen.save('uploads/' + nuevoNombreImagen)
        _imagen = nuevoNombreImagen

        sql = "SELECT image FROM movie WHERE id=%s"
        cursor.execute(sql, id)

        os.remove(app.config['UPLOADS'] + nombreFoto)
    else:
        _imagen = nombreFoto

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = f'UPDATE movie SET nombre="{_nombre}", descripcion="{_descripcion}", genero="{_genero}", image="{_imagen}" WHERE id={id}'
    cursor.execute(sql)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)