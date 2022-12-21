from flask import Flask, render_template
from flaskext.mysql import MySQL

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

    sql = "insert into movie (nombre,descripcion,genero,actores) values('titanic','boat that skins','boats','a lot of people');"
    cursor.execute(sql)

    conn.commit()

    return render_template('movies/index.html')

if __name__ == '__main__':
    app.run(debug=True)