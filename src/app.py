from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os

from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movies'
app.config['SECRET_KEY'] = 'appflask'

UPLOADS = os.path.join('uploads/')
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(cursor=DictCursor)

def queryMySql(query, data, tipoDeRetorno=None):
    if data != None:
        cursor.execute(query,data)
    else:
        cursor.execute(query)

    if tipoDeRetorno == "one":
        registro = cursor.fetchone()
    else:
        registro = cursor.fetchall()

    if query.casefold().find("select") != -1:
        conn.commit()
    
    return registro

@app.route('/moviepic/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/')
def index():

    sql = "SELECT * FROM movie;"
    cursor.execute(sql)

    movies = queryMySql(sql,None,"all")
    print(movies)

    conn.commit()

    return render_template('movies/index.html', movies = movies)

@app.route('/movie/create', methods=["GET","POST"])
def crear_pelicula():
    if request.method == "GET":
        return render_template('movies/create.html')
    elif request.method == "POST":
        _nombre = request.form['txtNombre']
        _descripcion = request.form['txtDesc']
        _genero = request.form['txtGene']
        _imagen = request.files['txtImg']

        if _nombre == '' or _descripcion == '':
            flash('Todos los campos son obligatorios')
            return redirect(url_for('crear_pelicula'))

        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        nuevoNombreImagen = ''

        if _imagen.filename != '':
            nuevoNombreImagen = tiempo + '_' + _imagen.filename
            _imagen.save('uploads/' + nuevoNombreImagen)

        sql = "INSERT INTO movie (nombre,descripcion,genero,image) values(%s, %s, %s, %s);"
        datos = (_nombre,_descripcion,_genero,nuevoNombreImagen)
        print(len(datos))

        queryMySql(sql,datos)

        return redirect('/')



@app.route('/delete/<int:id>')
def delete(id):
    
    sql = "SELECT image FROM movie WHERE id=(%s)"
    datos = (id,)
    nombreFoto = queryMySql(sql,datos,"one")['image']
    print(nombreFoto)
    
    try:
        os.remove(app.config['UPLOADS'] + nombreFoto)
    except:
        pass

    sql = "DELETE FROM movie WHERE id=(%s)"

    queryMySql(sql,datos)

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM movie WHERE id=%s"

    datos = (id,)

    movie = queryMySql(sql, datos, "one")
    print(movie)

    return render_template('movies/edit.html', movie=movie)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtDesc']
    _genero = request.form['txtGene']
    _imagen = request.files['txtImg']
    id = request.form['txtId']

    datos = (id,)
    print("linea 124", datos)
    
    sql = "SELECT image FROM movie WHERE id = (%s)"
    nombreFoto = queryMySql(sql, datos, "one")['image']

    if _imagen.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreImagen = tiempo + '_' + _imagen.filename
        _imagen.save('uploads/' + nuevoNombreImagen)
        _imagen = nuevoNombreImagen
        try:
            os.remove(app.config['UPLOADS'] + nombreFoto)
        except:
            pass
    else:
        _imagen = nombreFoto
    
    sql = "UPDATE movie SET nombre = (%s), descripcion = (%s), genero = (%s), image = (%s) WHERE id = (%s)"
    datos = (_nombre, _descripcion, _genero, _imagen, id)
    print("linea 143", datos)
    queryMySql(sql, datos)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)