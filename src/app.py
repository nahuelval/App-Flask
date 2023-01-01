from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movies'

mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM movie;"
    cursor.execute(sql)

    movies = cursor.fetchall()
    print(movies)

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

if __name__ == '__main__':
    app.run(debug=True)