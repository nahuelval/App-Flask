from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flaskext.mysql import MySQL
from datetime import datetime
from decouple import config
from PIL import Image
import os

from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_DATABASE_USER'] = config('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = config('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = config('MYSQL_DB')
app.config['SECRET_KEY'] = config('SECRET_KEY')

app.config['UPLOADS'] = config('UPLOADS')

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(cursor=DictCursor)


# FUNCIONES #

def queryMySql(query, data=None, tipoDeRetorno=None):
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

def selectSearch(name, desc, gene):
    count = 0

    if name != '':
        name = (name + '%')
        name = ("nombre LIKE CONCAT('%s')" % name)
        print(name)
        count += 1
    else:
        name = ''

    if desc != '':
        desc = (desc + '%')
        desc = ("descripcion LIKE CONCAT('%s')" % desc)
        if count > 0:
            desc = "AND " + desc
        print(desc)
    else:
        desc = ''

    if gene != '':
        gene = (gene + '%')
        gene = ("genero LIKE CONCAT('%s')" % gene)
        if count > 0:
            gene = "AND " + gene
        print(gene)
    else:
        gene = ''

    sqlQuery = ("SELECT * FROM movie WHERE (%s %s %s);" % (name,desc,gene))
    
    return sqlQuery


# RUTAS #

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/moviepic/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/')
def index():
    sql = "SELECT * FROM movie;"
    cursor.execute(sql)

    movies = queryMySql(sql,None)

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
            imagen = Image.open(_imagen)
            if imagen.width > 1920 and imagen.height > 1080:
                imagen = imagen.resize((1080, 1920))
            nuevoNombreImagen = tiempo + '_' + _imagen.filename
            imagen.save(app.config['UPLOADS'] + nuevoNombreImagen, optimize=True)

        sql = "INSERT INTO movie (nombre,descripcion,genero,image) values(%s, %s, %s, %s);"
        datos = (_nombre,_descripcion,_genero,nuevoNombreImagen)

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

    print(app.config['UPLOADS'] + nombreFoto)
    sql = "DELETE FROM movie WHERE id=(%s)"

    queryMySql(sql,datos)

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM movie WHERE id=%s"

    datos = (id,)

    movie = queryMySql(sql, datos, "one")

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
    queryMySql(sql, datos)

    return redirect('/')

@app.route('/buscar', methods=["GET","POST"])
def busqueda():
    _nombre = request.form['busqNombre']
    _descripcion = request.form['busqDescripcion']
    _genero = request.form['busqGenero']

    if _nombre == '' and _descripcion == '' and _genero == '':
        return redirect('/')

    sql = selectSearch(_nombre,_descripcion,_genero)

    print(sql)

    movies = queryMySql(sql)

    return render_template('movies/index.html', movies = movies)


if __name__ == '__main__':
    app.run(debug=True)